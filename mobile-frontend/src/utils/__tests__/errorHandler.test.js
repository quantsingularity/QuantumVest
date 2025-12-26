import {
    validateEmail,
    validatePassword,
    formatCurrency,
    formatNumber,
    formatPercentage,
} from '../errorHandler';

describe('Validation Functions', () => {
    describe('validateEmail', () => {
        it('validates correct email addresses', () => {
            expect(validateEmail('test@example.com')).toBe(true);
            expect(validateEmail('user.name@domain.co.uk')).toBe(true);
            expect(validateEmail('user+tag@example.org')).toBe(true);
        });

        it('rejects invalid email addresses', () => {
            expect(validateEmail('invalid')).toBe(false);
            expect(validateEmail('@example.com')).toBe(false);
            expect(validateEmail('user@')).toBe(false);
            expect(validateEmail('user @example.com')).toBe(false);
            expect(validateEmail('')).toBe(false);
        });
    });

    describe('validatePassword', () => {
        it('validates strong passwords', () => {
            expect(validatePassword('Password123')).toBe(true);
            expect(validatePassword('MyP@ssw0rd')).toBe(true);
            expect(validatePassword('Test1234')).toBe(true);
        });

        it('rejects weak passwords', () => {
            expect(validatePassword('password')).toBe(false); // no uppercase or number
            expect(validatePassword('PASSWORD123')).toBe(false); // no lowercase
            expect(validatePassword('Password')).toBe(false); // no number
            expect(validatePassword('Pass1')).toBe(false); // too short
            expect(validatePassword('')).toBe(false);
        });
    });
});

describe('Formatting Functions', () => {
    describe('formatCurrency', () => {
        it('formats currency with USD by default', () => {
            expect(formatCurrency(1234.56)).toBe('$1,234.56');
            expect(formatCurrency(0)).toBe('$0.00');
            expect(formatCurrency(999999.99)).toBe('$999,999.99');
        });

        it('formats currency with custom currency code', () => {
            expect(formatCurrency(1234.56, 'EUR')).toContain('1,234.56');
            expect(formatCurrency(1234.56, 'GBP')).toContain('1,234.56');
        });

        it('returns N/A for invalid values', () => {
            expect(formatCurrency('invalid')).toBe('N/A');
            expect(formatCurrency(null)).toBe('N/A');
            expect(formatCurrency(undefined)).toBe('N/A');
        });
    });

    describe('formatNumber', () => {
        it('formats numbers with default 2 decimals', () => {
            expect(formatNumber(1234.5678)).toBe('1,234.57');
            expect(formatNumber(1000)).toBe('1,000.00');
        });

        it('formats numbers with custom decimals', () => {
            expect(formatNumber(1234.5678, 0)).toBe('1,235');
            expect(formatNumber(1234.5678, 3)).toBe('1,234.568');
        });

        it('returns N/A for invalid values', () => {
            expect(formatNumber('invalid')).toBe('N/A');
            expect(formatNumber(null)).toBe('N/A');
        });
    });

    describe('formatPercentage', () => {
        it('formats positive percentages', () => {
            expect(formatPercentage(5.5)).toBe('+5.50%');
            expect(formatPercentage(10)).toBe('+10.00%');
        });

        it('formats negative percentages', () => {
            expect(formatPercentage(-5.5)).toBe('-5.50%');
            expect(formatPercentage(-10)).toBe('-10.00%');
        });

        it('formats zero', () => {
            expect(formatPercentage(0)).toBe('+0.00%');
        });

        it('returns N/A for invalid values', () => {
            expect(formatPercentage('invalid')).toBe('N/A');
            expect(formatPercentage(null)).toBe('N/A');
        });
    });
});
