

document.addEventListener('DOMContentLoaded', function () {
    var menuItems = document.querySelectorAll('.has-submenu > a');

    menuItems.forEach(function (menuItem) {
        menuItem.addEventListener('click', function (event) {
            event.preventDefault(); // Ngăn chặn hành vi mặc định của liên kết

            // Đóng tất cả các menu con khác
            var allSubmenus = document.querySelectorAll('.submenu');
            allSubmenus.forEach(function (submenu) {
                if (submenu !== menuItem.nextElementSibling) {
                    submenu.style.display = 'none';
                }
            });

            // Chuyển đổi hiển thị của menu con hiện tại
            var submenu = menuItem.nextElementSibling;
            if (submenu.style.display === 'block') {
                submenu.style.display = 'none';
            } else {
                submenu.style.display = 'block';
            }
        });
    });
});

