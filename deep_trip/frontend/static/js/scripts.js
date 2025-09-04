// 基础JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
    // 表单验证功能
    // 移除或注释掉全局表单提交拦截，避免影响后端交互
    /*
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            const requiredFields = this.querySelectorAll('[required]');
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                }
            });
            
            // 邮箱验证
            const emailFields = this.querySelectorAll('input[type="email"]');
            emailFields.forEach(field => {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (field.value && !emailPattern.test(field.value)) {
                    isValid = false;
                    field.classList.add('error');
                } else if (field.value) {
                    field.classList.remove('error');
                }
            });
            
            // 密码验证
            const passwordFields = this.querySelectorAll('input[type="password"]');
            passwordFields.forEach(field => {
                if (field.value && field.value.length < 6) {
                    isValid = false;
                    field.classList.add('error');
                } else if (field.value) {
                    field.classList.remove('error');
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showAlert('请填写正确的信息', 'danger');
            }
        });
    });
    */
    
    // 为所有带error类的输入框添加输入事件监听器
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            this.classList.remove('error');
        });
    });
    
    // 提示框功能
    function showAlert(message, type = 'info') {
        const alertContainer = document.createElement('div');
        alertContainer.className = `alert alert-${type}`;
        alertContainer.textContent = message;
        
        const mainContent = document.querySelector('main');
        if (mainContent) {
            const firstChild = mainContent.firstChild;
            if (firstChild) {
                mainContent.insertBefore(alertContainer, firstChild);
            } else {
                mainContent.appendChild(alertContainer);
            }
            
            // 3秒后自动移除提示框
            setTimeout(() => {
                alertContainer.remove();
            }, 3000);
        }
    }
    
    // 日期选择器增强
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        // 设置最小日期为今天
        const today = new Date().toISOString().split('T')[0];
        input.min = today;
    });
    
    // 平滑滚动
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // 加载状态指示器
    window.showLoading = function() {
        let loadingIndicator = document.getElementById('loading-indicator');
        if (!loadingIndicator) {
            loadingIndicator = document.createElement('div');
            loadingIndicator.id = 'loading-indicator';
            loadingIndicator.className = 'loading-overlay';
            loadingIndicator.innerHTML = `
                <div class="loading-spinner">
                    <div class="spinner"></div>
                    <p>加载中...</p>
                </div>
            `;
            document.body.appendChild(loadingIndicator);
        }
        loadingIndicator.style.display = 'flex';
    };
    
    window.hideLoading = function() {
        const loadingIndicator = document.getElementById('loading-indicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
    };
    
    // 确认对话框
    window.confirmDialog = function(message, callback) {
        if (confirm(message)) {
            if (typeof callback === 'function') {
                callback();
            }
            return true;
        }
        return false;
    };
    
    // 为删除按钮添加确认功能
    const deleteButtons = document.querySelectorAll('.btn-danger, .delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('确定要删除吗？此操作不可撤销。')) {
                e.preventDefault();
            }
        });
    });
    
    // 懒加载图片
    if ('IntersectionObserver' in window) {
        const imgObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    const src = img.getAttribute('data-src');
                    if (src) {
                        img.src = src;
                        img.removeAttribute('data-src');
                    }
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imgObserver.observe(img);
        });
    }
    
    // 添加加载动画的CSS
    const style = document.createElement('style');
    style.textContent = `
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(255, 255, 255, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 9999;
        }
        
        .loading-spinner {
            text-align: center;
        }
        
        .spinner {
            width: 40px;
            height: 40px;
            margin: 0 auto 20px;
            border: 4px solid #f3f3f3;
            border-top: 4px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        input.error, textarea.error, select.error {
            border-color: #dc3545;
        }
    `;
    document.head.appendChild(style);
});