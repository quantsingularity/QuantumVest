import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { authAPI, settingsAPI } from '../../services/api';
import { showToast } from '../ui/ToastManager';
import LoadingSpinner from '../ui/LoadingSpinner';

const Settings = () => {
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);

    // State for various settings
    const [notifications, setNotifications] = useState({
        email: true,
        push: true,
        sms: false,
    });

    const [theme, setTheme] = useState('system');
    const [language, setLanguage] = useState('english');
    const [currency, setCurrency] = useState('usd');
    const [twoFactorEnabled, setTwoFactorEnabled] = useState(false);

    // Personal information state
    const [personalInfo, setPersonalInfo] = useState({
        name: '',
        email: '',
        phone: '',
    });

    // Password change state
    const [passwordForm, setPasswordForm] = useState({
        current: '',
        new: '',
        confirm: '',
    });

    useEffect(() => {
        fetchUserData();
    }, []);

    const fetchUserData = async () => {
        try {
            setLoading(true);

            // Fetch user profile
            try {
                const profileResponse = await authAPI.getProfile();
                if (profileResponse.data.success && profileResponse.data.user) {
                    const user = profileResponse.data.user;
                    setPersonalInfo({
                        name:
                            `${user.first_name || ''} ${user.last_name || ''}`.trim() ||
                            user.username,
                        email: user.email || '',
                        phone: user.phone || '',
                    });

                    // Set currency preference if available
                    if (user.preferred_currency) {
                        setCurrency(user.preferred_currency.toLowerCase());
                    }
                }
            } catch (error) {
                console.warn('Could not fetch profile:', error);
                setPersonalInfo({
                    name: 'John Doe',
                    email: 'john.doe@example.com',
                    phone: '+1 (555) 123-4567',
                });
            }

            // Fetch settings
            try {
                const settingsResponse = await settingsAPI.getSettings();
                if (settingsResponse.data.success && settingsResponse.data.settings) {
                    const settings = settingsResponse.data.settings;
                    setNotifications({
                        email: settings.email_notifications !== false,
                        push: settings.push_notifications !== false,
                        sms: settings.sms_notifications !== false,
                    });
                    setTwoFactorEnabled(settings.two_factor_enabled || false);
                }
            } catch (error) {
                console.warn('Could not fetch settings:', error);
            }
        } catch (error) {
            console.error('Error fetching user data:', error);
            showToast('Could not load settings. Using defaults.', 'warning');
        } finally {
            setLoading(false);
        }
    };

    // Handle notification toggle
    const handleNotificationToggle = (type) => {
        setNotifications({
            ...notifications,
            [type]: !notifications[type],
        });
    };

    // Handle personal info change
    const handlePersonalInfoChange = (e) => {
        const { name, value } = e.target;
        setPersonalInfo({
            ...personalInfo,
            [name]: value,
        });
    };

    // Handle password change
    const handlePasswordChange = (e) => {
        const { name, value } = e.target;
        setPasswordForm({
            ...passwordForm,
            [name]: value,
        });
    };

    // Handle form submission
    const handleSubmit = async (e, formType) => {
        e.preventDefault();
        setSaving(true);

        try {
            if (formType === 'Account') {
                const [firstName, ...lastNameParts] = personalInfo.name.split(' ');
                const lastName = lastNameParts.join(' ');

                const updateData = {
                    first_name: firstName,
                    last_name: lastName,
                    phone: personalInfo.phone,
                };

                const response = await authAPI.updateProfile(updateData);

                if (response.data.success) {
                    showToast('Account settings updated successfully!', 'success');
                } else {
                    throw new Error(response.data.error || 'Update failed');
                }
            } else if (formType === 'Password') {
                if (passwordForm.new !== passwordForm.confirm) {
                    showToast('New passwords do not match', 'error');
                    setSaving(false);
                    return;
                }

                if (passwordForm.new.length < 8) {
                    showToast('Password must be at least 8 characters long', 'error');
                    setSaving(false);
                    return;
                }

                const response = await settingsAPI.changePassword({
                    current_password: passwordForm.current,
                    new_password: passwordForm.new,
                });

                if (response.data.success) {
                    showToast('Password updated successfully!', 'success');
                    setPasswordForm({
                        current: '',
                        new: '',
                        confirm: '',
                    });
                } else {
                    throw new Error(response.data.error || 'Password update failed');
                }
            } else if (formType === 'Preferences') {
                const response = await settingsAPI.updateSettings({
                    theme: theme,
                    language: language,
                    preferred_currency: currency.toUpperCase(),
                });

                if (response.data.success) {
                    showToast('Preferences saved successfully!', 'success');
                } else {
                    throw new Error(response.data.error || 'Update failed');
                }
            } else if (formType === 'Notifications') {
                const response = await settingsAPI.updateSettings({
                    email_notifications: notifications.email,
                    push_notifications: notifications.push,
                    sms_notifications: notifications.sms,
                });

                if (response.data.success) {
                    showToast('Notification settings updated successfully!', 'success');
                } else {
                    throw new Error(response.data.error || 'Update failed');
                }
            }
        } catch (error) {
            console.error(`Error updating ${formType}:`, error);
            showToast(
                error.response?.data?.error ||
                    error.message ||
                    `Failed to update ${formType.toLowerCase()} settings`,
                'error',
            );
        } finally {
            setSaving(false);
        }
    };

    const handleTwoFactorToggle = async () => {
        try {
            setSaving(true);
            const newValue = !twoFactorEnabled;

            const response = newValue
                ? await settingsAPI.enable2FA()
                : await settingsAPI.disable2FA();

            if (response.data.success) {
                setTwoFactorEnabled(newValue);
                showToast(
                    `Two-factor authentication ${newValue ? 'enabled' : 'disabled'} successfully!`,
                    'success',
                );
            } else {
                throw new Error(response.data.error || '2FA toggle failed');
            }
        } catch (error) {
            console.error('Error toggling 2FA:', error);
            showToast(
                error.response?.data?.error || 'Failed to update two-factor authentication',
                'error',
            );
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return (
            <div className="loading-container">
                <LoadingSpinner text="Loading settings" />
            </div>
        );
    }

    return (
        <div className="settings-page">
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
            >
                <h2 className="section-title">Settings</h2>

                <div className="grid grid-2">
                    {/* Account Settings */}
                    <motion.div
                        className="card"
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.1, duration: 0.5 }}
                    >
                        <h3 className="card-title">Account Settings</h3>

                        <form onSubmit={(e) => handleSubmit(e, 'Account')}>
                            <div className="form-group">
                                <label className="form-label">Full Name</label>
                                <input
                                    type="text"
                                    className="form-control"
                                    name="name"
                                    value={personalInfo.name}
                                    onChange={handlePersonalInfoChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Email Address</label>
                                <input
                                    type="email"
                                    className="form-control"
                                    name="email"
                                    value={personalInfo.email}
                                    onChange={handlePersonalInfoChange}
                                    disabled
                                    title="Email cannot be changed"
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Phone Number</label>
                                <input
                                    type="tel"
                                    className="form-control"
                                    name="phone"
                                    value={personalInfo.phone}
                                    onChange={handlePersonalInfoChange}
                                />
                            </div>

                            <button type="submit" className="btn btn-primary" disabled={saving}>
                                {saving ? 'Saving...' : 'Save Changes'}
                            </button>
                        </form>
                    </motion.div>

                    {/* Security Settings */}
                    <motion.div
                        className="card"
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: 0.2, duration: 0.5 }}
                    >
                        <h3 className="card-title">Security</h3>

                        <form onSubmit={(e) => handleSubmit(e, 'Password')}>
                            <div className="form-group">
                                <label className="form-label">Current Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="current"
                                    value={passwordForm.current}
                                    onChange={handlePasswordChange}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">New Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="new"
                                    value={passwordForm.new}
                                    onChange={handlePasswordChange}
                                    required
                                    minLength="8"
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Confirm New Password</label>
                                <input
                                    type="password"
                                    className="form-control"
                                    name="confirm"
                                    value={passwordForm.confirm}
                                    onChange={handlePasswordChange}
                                    required
                                    minLength="8"
                                />
                            </div>

                            <button type="submit" className="btn btn-primary" disabled={saving}>
                                {saving ? 'Updating...' : 'Update Password'}
                            </button>
                        </form>

                        <hr className="my-4" style={{ margin: '2rem 0' }} />

                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h4 className="mb-1">Two-Factor Authentication</h4>
                                <p className="text-secondary mb-0">
                                    Add an extra layer of security to your account
                                </p>
                            </div>
                            <div className="form-check form-switch">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    checked={twoFactorEnabled}
                                    onChange={handleTwoFactorToggle}
                                    disabled={saving}
                                    style={{
                                        width: '48px',
                                        height: '24px',
                                        cursor: saving ? 'not-allowed' : 'pointer',
                                        appearance: 'none',
                                        backgroundColor: twoFactorEnabled
                                            ? 'var(--success-color)'
                                            : 'var(--light-gray)',
                                        borderRadius: '12px',
                                        position: 'relative',
                                        transition: 'var(--transition)',
                                    }}
                                />
                            </div>
                        </div>
                    </motion.div>

                    {/* Preferences */}
                    <motion.div
                        className="card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.3, duration: 0.5 }}
                    >
                        <h3 className="card-title">Preferences</h3>

                        <div className="form-group">
                            <label className="form-label">Theme</label>
                            <select
                                className="form-control"
                                value={theme}
                                onChange={(e) => setTheme(e.target.value)}
                            >
                                <option value="light">Light</option>
                                <option value="dark">Dark</option>
                                <option value="system">System Default</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label className="form-label">Language</label>
                            <select
                                className="form-control"
                                value={language}
                                onChange={(e) => setLanguage(e.target.value)}
                            >
                                <option value="english">English</option>
                                <option value="spanish">Spanish</option>
                                <option value="french">French</option>
                                <option value="german">German</option>
                                <option value="chinese">Chinese</option>
                            </select>
                        </div>

                        <div className="form-group">
                            <label className="form-label">Currency</label>
                            <select
                                className="form-control"
                                value={currency}
                                onChange={(e) => setCurrency(e.target.value)}
                            >
                                <option value="usd">USD ($)</option>
                                <option value="eur">EUR (€)</option>
                                <option value="gbp">GBP (£)</option>
                                <option value="jpy">JPY (¥)</option>
                                <option value="cny">CNY (¥)</option>
                            </select>
                        </div>

                        <button
                            className="btn btn-primary"
                            onClick={(e) => handleSubmit(e, 'Preferences')}
                            disabled={saving}
                        >
                            {saving ? 'Saving...' : 'Save Preferences'}
                        </button>
                    </motion.div>

                    {/* Notifications */}
                    <motion.div
                        className="card"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{ delay: 0.4, duration: 0.5 }}
                    >
                        <h3 className="card-title">Notifications</h3>

                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h4 className="mb-1">Email Notifications</h4>
                                <p className="text-secondary mb-0">
                                    Receive updates and alerts via email
                                </p>
                            </div>
                            <div className="form-check form-switch">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    checked={notifications.email}
                                    onChange={() => handleNotificationToggle('email')}
                                    style={{
                                        width: '48px',
                                        height: '24px',
                                        cursor: 'pointer',
                                        appearance: 'none',
                                        backgroundColor: notifications.email
                                            ? 'var(--success-color)'
                                            : 'var(--light-gray)',
                                        borderRadius: '12px',
                                        position: 'relative',
                                        transition: 'var(--transition)',
                                    }}
                                />
                            </div>
                        </div>

                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h4 className="mb-1">Push Notifications</h4>
                                <p className="text-secondary mb-0">
                                    Receive notifications in your browser
                                </p>
                            </div>
                            <div className="form-check form-switch">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    checked={notifications.push}
                                    onChange={() => handleNotificationToggle('push')}
                                    style={{
                                        width: '48px',
                                        height: '24px',
                                        cursor: 'pointer',
                                        appearance: 'none',
                                        backgroundColor: notifications.push
                                            ? 'var(--success-color)'
                                            : 'var(--light-gray)',
                                        borderRadius: '12px',
                                        position: 'relative',
                                        transition: 'var(--transition)',
                                    }}
                                />
                            </div>
                        </div>

                        <div className="d-flex justify-content-between align-items-center mb-3">
                            <div>
                                <h4 className="mb-1">SMS Notifications</h4>
                                <p className="text-secondary mb-0">
                                    Receive important alerts via SMS
                                </p>
                            </div>
                            <div className="form-check form-switch">
                                <input
                                    className="form-check-input"
                                    type="checkbox"
                                    checked={notifications.sms}
                                    onChange={() => handleNotificationToggle('sms')}
                                    style={{
                                        width: '48px',
                                        height: '24px',
                                        cursor: 'pointer',
                                        appearance: 'none',
                                        backgroundColor: notifications.sms
                                            ? 'var(--success-color)'
                                            : 'var(--light-gray)',
                                        borderRadius: '12px',
                                        position: 'relative',
                                        transition: 'var(--transition)',
                                    }}
                                />
                            </div>
                        </div>

                        <button
                            className="btn btn-primary"
                            onClick={(e) => handleSubmit(e, 'Notifications')}
                            disabled={saving}
                        >
                            {saving ? 'Saving...' : 'Save Notification Settings'}
                        </button>
                    </motion.div>
                </div>

                {/* Danger Zone */}
                <motion.div
                    className="card mt-4"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: 0.5, duration: 0.5 }}
                    style={{ borderColor: 'var(--danger-color)' }}
                >
                    <h3 className="card-title text-danger">Danger Zone</h3>

                    <div className="d-flex justify-content-between align-items-center">
                        <div>
                            <h4 className="mb-1">Delete Account</h4>
                            <p className="text-secondary mb-0">
                                Permanently delete your account and all associated data
                            </p>
                        </div>
                        <button
                            className="btn btn-danger"
                            onClick={() =>
                                showToast(
                                    'Account deletion requires confirmation. Please contact support.',
                                    'warning',
                                )
                            }
                        >
                            Delete Account
                        </button>
                    </div>
                </motion.div>
            </motion.div>
        </div>
    );
};

export default Settings;
