/**
 * DataLab Dashboard – Global Interactions
 * Linked via: {{ url_for('static', filename='js/script.js') }} in base.html
 */

(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {

        /* ── Mobile Sidebar Toggle ─────────────────────────── */
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebar = document.getElementById('sidebar');
        const sidebarOverlay = document.getElementById('sidebarOverlay');

        function openSidebar() {
            if (!sidebar) return;
            sidebar.classList.add('open');
            sidebarOverlay.classList.add('active');
            document.body.style.overflow = 'hidden';
        }

        function closeSidebar() {
            if (!sidebar) return;
            sidebar.classList.remove('open');
            sidebarOverlay.classList.remove('active');
            document.body.style.overflow = '';
        }

        if (sidebarToggle) {
            sidebarToggle.addEventListener('click', function () {
                sidebar && sidebar.classList.contains('open')
                    ? closeSidebar()
                    : openSidebar();
            });
        }

        if (sidebarOverlay) {
            sidebarOverlay.addEventListener('click', closeSidebar);
        }

        /* Close sidebar when a nav link is clicked (mobile) */
        if (sidebar) {
            sidebar.querySelectorAll('.nav-item').forEach(function (link) {
                link.addEventListener('click', closeSidebar);
            });
        }

        /* ── Auto-dismiss Flash Messages after 5 s ─────────── */
        document.querySelectorAll('.flash-alert').forEach(function (alert) {
            setTimeout(function () {
                alert.style.transition = 'opacity .4s';
                alert.style.opacity = '0';
                setTimeout(function () { alert.remove(); }, 400);
            }, 5000);
        });

        console.info('DataLab initialised.');
    });

}());
