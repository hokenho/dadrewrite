// Shared navigation bar – included by all pages
(function () {
    var page = location.pathname.split('/').pop() || 'index.html';

    var groups = [
        { label: 'Signer Authorization', href: 'signer.html' },
        { label: 'Signer Onboarding', children: [
            { label: 'Request New Signer', href: 'request_signer.html' },
            { label: 'Signer Request Status', href: 'request_status.html' }
        ]},
        { label: 'Tables Administration', children: [
            { label: 'Policies', href: 'policy.html' },
            { label: 'Business Units', href: 'bu.html' },
            { label: 'Cost Centres', href: 'cc.html' },
            { label: 'Countries', href: 'country.html' },
            { label: 'Currencies', href: 'currency.html' },
            { label: 'Exchange Rates', href: 'exrate.html' },
            { label: 'Job Levels', href: 'joblevel.html' }
        ]},
        { label: 'Reports', children: [
            { label: 'Reports and Extracts', href: '#' }
        ]},
        { label: 'Utilities', children: [
            { label: 'Upload Tool', href: 'upload.html' },
            { label: 'Dashboard', href: 'dashboard.html' }
        ]}
    ];

    function isActive(group) {
        if (group.href) return group.href === page;
        if (group.children) return group.children.some(function (c) { return c.href === page; });
        return false;
    }

    var nav = document.createElement('nav');
    nav.className = 'navbar';

    // Main Menu as first nav item
    var mainDiv = document.createElement('div');
    mainDiv.className = 'nav-group';
    var mainLink = document.createElement('a');
    mainLink.className = 'nav-group-label' + (page === 'index.html' ? ' active' : '');
    mainLink.href = 'index.html';
    mainLink.textContent = 'Main Menu';
    mainDiv.appendChild(mainLink);
    nav.appendChild(mainDiv);

    groups.forEach(function (g) {
        var div = document.createElement('div');
        div.className = 'nav-group';

        if (g.href) {
            var a = document.createElement('a');
            a.className = 'nav-group-label' + (isActive(g) ? ' active' : '');
            a.href = g.href;
            a.textContent = g.label;
            div.appendChild(a);
        } else {
            var span = document.createElement('span');
            span.className = 'nav-group-label' + (isActive(g) ? ' active' : '');
            span.textContent = g.label;
            div.appendChild(span);

            var dd = document.createElement('div');
            dd.className = 'nav-dropdown';
            g.children.forEach(function (c) {
                var link = document.createElement('a');
                link.href = c.href;
                link.textContent = c.label;
                dd.appendChild(link);
            });
            div.appendChild(dd);
        }

        nav.appendChild(div);
    });

    // Spacer
    var spacer = document.createElement('div');
    spacer.className = 'nav-spacer';
    nav.appendChild(spacer);

    // My Alerts button (all pages)
    var alertsBtn = document.createElement('button');
    alertsBtn.id = 'alertsBtn';
    alertsBtn.className = 'nav-btn alerts-btn';
    alertsBtn.setAttribute('onclick', 'toggleAlertPanel()');
    alertsBtn.innerHTML =
        '<svg class="alerts-btn-icon--active" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>' +
        ' <strong>My Alerts</strong> ' +
        '<span class="alerts-badge">5</span>';
    nav.appendChild(alertsBtn);

    // Logout button
    var logout = document.createElement('a');
    logout.className = 'logout-link';
    logout.href = 'logout.html';
    logout.textContent = 'Logout';
    nav.appendChild(logout);

    // Insert after .page-header
    var header = document.querySelector('.page-header');
    if (header && header.nextSibling) {
        header.parentNode.insertBefore(nav, header.nextSibling);
    } else {
        document.querySelector('.container').appendChild(nav);
    }

    // Inject alerts overlay + panel + toggle function (shared across all pages)
    if (!document.getElementById('alertsOverlay')) {
        var overlay = document.createElement('div');
        overlay.id = 'alertsOverlay';
        overlay.className = 'alerts-overlay';
        overlay.setAttribute('onclick', 'toggleAlertPanel()');
        document.body.appendChild(overlay);

        var panel = document.createElement('div');
        panel.id = 'alertsPanel';
        panel.className = 'alerts-panel';
        panel.innerHTML =
            '<div class="alerts-panel-header">' +
                '<span>' +
                    '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px;margin-right:6px"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>My Alerts' +
                '</span>' +
                '<button class="alerts-panel-close" onclick="toggleAlertPanel()" title="Close">&#x2715;</button>' +
            '</div>' +
            '<ul class="alerts-list">' +
                '<li class="alerts-list-item"><a href="request_status.html?highlight=user_upn@manulife.com" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#27ae60" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg><span>Signer Change Approved</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; GDAS</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; Infor</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; Workday</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html?highlight=user_upn@manulife.com" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg><span>Pending Signer Change</span></a></li>' +
            '</ul>';
        document.body.appendChild(panel);

        window.toggleAlertPanel = function () {
            var p = document.getElementById('alertsPanel');
            var o = document.getElementById('alertsOverlay');
            var open = p.classList.toggle('alerts-panel--open');
            o.classList.toggle('alerts-overlay--visible', open);
        };
    }
})();

