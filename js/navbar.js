// Shared navigation bar – included by all pages
(function () {
    var page = location.pathname.split('/').pop() || 'index.html';

    var groups = [
        { label: 'Signer Authorization', href: 'signer.html' },
        { label: 'Signer Onboarding', children: [
            { label: 'Request New Signer', href: 'request_signer.html' },
            { label: 'Signer Request Status', href: 'request_status.html' },
            { label: 'Signer Request Approval (AVP+)', href: 'req_approval.html?mode=approver1' }
        ]},
        { label: 'Tables Administration', children: [
            { label: 'Policies Categories', href: 'table_policy.html' },
            { label: 'Countries/Territories', href: 'table_country.html' },
            { label: 'Business Units', href: 'table_bu.html' },
            { label: 'Cost Centres', href: 'table_cc.html' },
            { label: 'Currencies', href: 'table_currency.html' },
            { label: 'Exchange Rates', href: 'table_exrate.html' },
            { label: 'Job Levels', href: 'table_joblevel.html' }
        ]},
        { label: 'Reports', children: [
            { label: 'Reports and Extracts', href: 'report.html' }
        ]},
        { label: 'Utilities', children: [
            { label: 'Dashboard', href: 'dashboard.html' },
            { label: 'Signer Request Approval (TSA)', href: 'req_approval.html?mode=approver2' },
            { label: 'User Access', href: 'user_access.html' },
            { label: 'Upload Tool', href: 'upload.html' }
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

    // Mode switch buttons (index.html only) — before My Alerts
    if (page === 'index.html') {
        var modes = [
            { label: 'Public User View', param: 'public_user' },
            { label: 'DAD User View', param: 'dad_user' },
            { label: 'TSA User View', param: 'tsa' }
        ];
        modes.forEach(function(m) {
            var btn = document.createElement('button');
            btn.className = 'nav-btn';
            btn.style.cssText = 'background:#6a1b9a;color:#fff;border:none;padding:4px 12px;border-radius:4px;font-size:0.78rem;font-weight:600;cursor:pointer;margin-left:6px;';
            btn.textContent = m.label;
            btn.addEventListener('click', function() {
                window.location.href = 'index.html?mode=' + m.param;
            });
            nav.appendChild(btn);
        });
    }

    // My Alerts button (all pages)
    var alertsBtn = document.createElement('button');
    alertsBtn.id = 'alertsBtn';
    alertsBtn.className = 'nav-btn alerts-btn';
    alertsBtn.setAttribute('onclick', 'toggleAlertPanel()');
    alertsBtn.innerHTML =
        '<svg class="alerts-btn-icon--active" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>' +
        ' <strong>My Alerts</strong> ' +
        '<span class="alerts-badge">4</span>';
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
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; Policies Categories</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; Cost Centres</span></a></li>' +
                '<li class="alerts-list-item"><a href="dashboard.html" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 5v4c0 1.66-4.03 3-9 3S3 10.66 3 9V5"/><path d="M21 13v4c0 1.66-4.03 3-9 3S3 18.66 3 17v-4"/></svg><span>Source Data Change &ndash; Workday User</span></a></li>' +
                '<li class="alerts-list-item"><a href="signer_details.html?action=view_request&id=100001" class="alerts-link"><svg class="alerts-item-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg><span>Pending Change: DADREQ100001</span></a></li>' +
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

