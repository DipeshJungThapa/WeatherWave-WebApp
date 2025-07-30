// Custom hook for enhanced form management
import { useState, useCallback } from 'react';

export const useAuthForm = (initialState = {}) => {
    const [formData, setFormData] = useState(initialState);
    const [errors, setErrors] = useState({});
    const [touched, setTouched] = useState({});

    const updateField = useCallback((name, value) => {
        setFormData(prev => ({ ...prev, [name]: value }));
        
        // Clear error when user starts typing
        if (errors[name]) {
            setErrors(prev => {
                const newErrors = { ...prev };
                delete newErrors[name];
                return newErrors;
            });
        }
    }, [errors]);

    const setFieldError = useCallback((name, error) => {
        setErrors(prev => ({ ...prev, [name]: error }));
    }, []);

    const clearErrors = useCallback(() => {
        setErrors({});
    }, []);

    const setFieldTouched = useCallback((name) => {
        setTouched(prev => ({ ...prev, [name]: true }));
    }, []);

    const resetForm = useCallback(() => {
        setFormData(initialState);
        setErrors({});
        setTouched({});
    }, [initialState]);

    const validateField = useCallback((name, value, validationRules = {}) => {
        const rules = validationRules[name];
        if (!rules) return;

        let error = '';

        // Required validation
        if (rules.required && (!value || value.trim() === '')) {
            error = rules.requiredMessage || `${name} is required`;
        }
        
        // Min length validation
        if (!error && rules.minLength && value.length < rules.minLength) {
            error = rules.minLengthMessage || `${name} must be at least ${rules.minLength} characters`;
        }

        // Email validation
        if (!error && rules.email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(value)) {
                error = rules.emailMessage || 'Please enter a valid email address';
            }
        }

        // Custom validation
        if (!error && rules.custom) {
            error = rules.custom(value, formData);
        }

        if (error) {
            setFieldError(name, error);
            return false;
        }

        return true;
    }, [formData, setFieldError]);

    const isValid = Object.keys(errors).length === 0;

    return {
        formData,
        errors,
        touched,
        isValid,
        updateField,
        setFieldError,
        clearErrors,
        setFieldTouched,
        resetForm,
        validateField
    };
};

// Validation rules helper
export const createValidationRules = () => ({
    username: {
        required: true,
        minLength: 3,
        requiredMessage: 'Username is required',
        minLengthMessage: 'Username must be at least 3 characters'
    },
    email: {
        required: true,
        email: true,
        requiredMessage: 'Email is required',
        emailMessage: 'Please enter a valid email address'
    },
    password: {
        required: true,
        minLength: 8,
        requiredMessage: 'Password is required',
        minLengthMessage: 'Password must be at least 8 characters',
        custom: (value) => {
            const hasUpper = /[A-Z]/.test(value);
            const hasLower = /[a-z]/.test(value);
            const hasNumber = /[0-9]/.test(value);
            
            if (!hasUpper || !hasLower || !hasNumber) {
                return 'Password must contain uppercase, lowercase, and number';
            }
            return null;
        }
    },
    confirmPassword: {
        required: true,
        custom: (value, formData) => {
            if (value !== formData.password) {
                return 'Passwords do not match';
            }
            return null;
        }
    }
});
