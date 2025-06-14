document.addEventListener('DOMContentLoaded', function () {
    // Toggle password visibility
    const toggleLoginPassword = document.getElementById('toggleLoginPassword');
    if (toggleLoginPassword) {
        toggleLoginPassword.addEventListener('click', function () {
            const passwordInput = document.getElementById('login-password');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }

    const toggleSigninPassword = document.getElementById('toggleSigninPassword');
    if (toggleSigninPassword) {
        toggleSigninPassword.addEventListener('click', function () {
            const passwordInput = document.getElementById('signup-password');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }
    
    const toggleCSigninPassword = document.getElementById('toggleCSigninPassword');
    if (toggleCSigninPassword) {
        toggleCSigninPassword.addEventListener('click', function () {
            const passwordInput = document.getElementById('signup-confirm');
            if (passwordInput.type === 'password') {
                passwordInput.type = 'text';
                this.classList.remove('fa-eye');
                this.classList.add('fa-eye-slash');
            } else {
                passwordInput.type = 'password';
                this.classList.remove('fa-eye-slash');
                this.classList.add('fa-eye');
            }
        });
    }

    // Handle tab switching
    const loginTab = document.getElementById('login-tab');
    const signupTab = document.getElementById('signup-tab');
    const loginForm = document.getElementById('login-form');
    const signupForm = document.getElementById('signup-form');
    const forgotForm = document.getElementById('forgot-form');

    loginTab.addEventListener('click', () => {
        loginTab.classList.add('active');
        signupTab.classList.remove('active');
        loginForm.classList.add('active');
        signupForm.classList.remove('active');
        forgotForm.classList.remove('active');
    });

    signupTab.addEventListener('click', () => {
        signupTab.classList.add('active');
        loginTab.classList.remove('active');
        signupForm.classList.add('active');
        loginForm.classList.remove('active');
        forgotForm.classList.remove('active');
    });

    // Handle forgot password link
    const forgotPassword = document.getElementById('forgot-password');
    const backToLogin = document.getElementById('back-to-login');

    forgotPassword.addEventListener('click', (e) => {
        e.preventDefault();
        loginForm.classList.remove('active');
        forgotForm.classList.add('active');
    });

    backToLogin.addEventListener('click', (e) => {
        e.preventDefault();
        forgotForm.classList.remove('active');
        loginForm.classList.add('active');
    });
});
