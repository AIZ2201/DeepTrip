// 基础JavaScript功能

document.addEventListener('DOMContentLoaded', function() {
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
    
    // 辅助方法：将 shop_info 数据填入表单输入框（强制覆盖）
    window.fillFormWithShopInfo = function(info) {
        if (!info) return;
        // 基本信息
        const elName = document.getElementById('shop-name');
        if (elName) elName.value = info.name ?? '';
        const elCategory = document.getElementById('shop-category');
        if (elCategory) elCategory.value = info.category ?? '';
        const elPriceRange = document.getElementById('shop-price-range');
        if (elPriceRange) elPriceRange.value = info.price_range ?? '';
        const elDesc = document.getElementById('shop-description');
        if (elDesc) elDesc.value = info.description ?? '';
        // 位置信息
        const elAddress = document.getElementById('shop-address');
        if (elAddress) elAddress.value = info.address ?? '';
        const elCity = document.getElementById('shop-city');
        if (elCity) elCity.value = info.city ?? '';
        const elDistrict = document.getElementById('shop-district');
        if (elDistrict) elDistrict.value = info.district ?? '';
        // 联系方式
        const elPhone = document.getElementById('shop-phone');
        if (elPhone) elPhone.value = info.phone ?? '';
        const elEmail = document.getElementById('shop-email');
        if (elEmail) elEmail.value = info.email ?? '';
        const elWebsite = document.getElementById('shop-website');
        if (elWebsite) elWebsite.value = info.website ?? '';
        const elWechat = document.getElementById('shop-wechat');
        if (elWechat) elWechat.value = info.wechat ?? '';
        // 节假日说明
        const elHoliday = document.getElementById('shop-holiday-info');
        if (elHoliday) elHoliday.value = info.holiday_info ?? '';
        // 营业时间
        if (info.business_hours) {
            info.business_hours.forEach(function(bh, idx){
                var i = idx + 1;
                var toggle = document.querySelector('.day-toggle[data-day="' + i + '"]');
                var start = document.querySelector('.business-hour-start[data-day="' + i + '"]');
                var end = document.querySelector('.business-hour-end[data-day="' + i + '"]');
                if (toggle && typeof bh.isOpen !== 'undefined') toggle.checked = bh.isOpen;
                if (start && bh.startTime) start.value = bh.startTime;
                if (end && bh.endTime) end.value = bh.endTime;
                if (toggle && !toggle.checked) {
                    if (start) start.disabled = true;
                    if (end) end.disabled = true;
                } else {
                    if (start) start.disabled = false;
                    if (end) end.disabled = false;
                }
            });
        }
        // 服务项目
        var container = document.getElementById('service-items-container');
        if (container && info.service_items && info.service_items.length > 0) {
            container.innerHTML = '';
            info.service_items.forEach(function(item){
                var div = document.createElement('div');
                div.className = 'service-item';
                div.innerHTML = `<input type="text" placeholder="服务名称" class="service-name" value="${item.name ?? ''}">` +
                    `<input type="number" placeholder="价格（元）" class="service-price" min="0" step="0.01" value="${item.price ?? ''}">` +
                    `<button type="button" class="remove-service-item">删除</button>`;
                container.appendChild(div);
                div.querySelector('.remove-service-item').onclick = function(){ div.remove(); };
            });
        }
        // 图片预览
        var imgContainer = document.getElementById('image-preview-container');
        if (imgContainer && info.images && info.images.length > 0) {
            imgContainer.innerHTML = '';
            info.images.forEach(function(url){
                var div = document.createElement('div');
                div.className = 'image-preview';
                div.innerHTML = `<img src="${url}" alt="图片预览"><button type="button" class="image-preview-remove">×</button>`;
                div.querySelector('.image-preview-remove').onclick = function(){ div.remove(); };
                imgContainer.appendChild(div);
            });
        }
        // 填充完后去除所有 error 类
        document.querySelectorAll('input, textarea, select').forEach(el => {
            el.classList.remove('error');
        });
    };
});
