// Shared DADREQ data loader — loads from signer_req + audit_dadreq via sql.js
//   window.DADREQ_LIST  — array of all entries (open + closed)
//   window.DADREQ_MAP   — keyed by reqId (for signer_details.html)
//   window.DADREQ_READY — Promise that resolves when data is loaded
(function() {
    window.DADREQ_LIST = [];
    window.DADREQ_MAP  = {};

    window.DADREQ_READY = initSqlJs({
        locateFile: function(file) { return 'js/sql-js/' + file; }
    }).then(function(SQL) {
        return fetch('db/data.db').then(function(resp) { return resp.arrayBuffer(); }).then(function(buf) {
            var db = new SQL.Database(new Uint8Array(buf));

            // Load Open requests from signer_req + signer_limit_req
            var openResults = db.exec(
                "SELECT o.id, o.req_date, o.submitter, o.gad_id, " +
                "l.id as lid, l.action, l.source_id, l.territory_id, l.policy_id, l.limit_amount, " +
                "l.approval_cc_id, l.exception, l.temp, l.temp_start_date, l.temp_end_date, l.business_rationale, l.business_control, " +
                "l.account_restriction, l.currency " +
                "FROM signer_req o LEFT JOIN signer_limit_req l ON l.signer_req_id = o.id ORDER BY o.id"
            );

            // Territory id -> code lookup
            var terrMap = {};
            var terrRes = db.exec("SELECT id, country_code FROM territory");
            if (terrRes.length) terrRes[0].values.forEach(function(r) { terrMap[r[0]] = r[1]; });

            // Cost center id -> cc lookup
            var ccMap = {};
            var ccRes = db.exec("SELECT id, cc FROM cost_center");
            if (ccRes.length) ccRes[0].values.forEach(function(r) { ccMap[r[0]] = r[1]; });

            // Policy id -> category, system lookup
            var policyMap = {};
            var policyRes = db.exec("SELECT id, category, system FROM policy");
            if (policyRes.length) policyRes[0].values.forEach(function(r) { policyMap[r[0]] = { cat: r[1], sys: r[2] }; });

            // Group open limits by request id
            var openMap = {};
            if (openResults.length) {
                openResults[0].values.forEach(function(r) {
                    var reqNum = r[0];
                    if (!openMap[reqNum]) {
                        openMap[reqNum] = {
                            id: reqNum, date: r[1], submitter: r[2], submittedFor: r[3],
                            limits: []
                        };
                    }
                    if (r[4] !== null) {
                        var actionMap = { 'Change': 'update', 'Remove': 'delete', 'Add': 'new' };
                        var limEntry = { type: actionMap[r[5]] || r[5] };
                        if (r[6] !== null) limEntry.rowIndex = r[6];
                        if (r[5] !== 'Remove') {
                            var amt = r[9] ? Number(r[9]).toLocaleString() : '0';
                            var pol = policyMap[r[8]] || {};
                            limEntry.newData = [
                                terrMap[r[7]] || '', pol.cat || '', amt, r[18] || '',
                                ccMap[r[10]] || '', r[11] ? 'Y' : 'N', r[12] ? 'Y' : 'N',
                                r[13] || '\u2014', r[14] || '\u2014',
                                r[15] ? 'Y' : 'N', r[16] ? 'Y' : 'N', pol.sys || '', r[17] || ''
                            ];
                        }
                        openMap[reqNum].limits.push(limEntry);
                    }
                });
            }

            // Add open requests to lists
            Object.keys(openMap).forEach(function(key) {
                var o = openMap[key];
                var reqId = 'DADREQ' + o.id;
                var entry = {
                    reqId: reqId, date: o.date, submitter: o.submitter,
                    submittedFor: o.submittedFor, status: 'Open', reason: '',
                    profile: {}, limits: o.limits
                };
                window.DADREQ_LIST.push(entry);
                window.DADREQ_MAP[reqId] = {
                    requestStatus: 'Open', requester: o.submitter, reason: '',
                    profile: {}, limits: o.limits
                };
            });

            // Load closed requests from audit_dadreq
            var auditResults = db.exec(
                "SELECT id, gad_id, req_date, submitter, status, reason, data_old, data_new FROM audit_dadreq ORDER BY id"
            );
            if (auditResults.length) {
                auditResults[0].values.forEach(function(r) {
                    var dataNew = r[7] ? JSON.parse(r[7]) : {};
                    var profile = dataNew.profile || {};
                    var limits = dataNew.limits || [];
                    var reqId = 'DADREQ' + (200000 + r[0]);
                    var entry = {
                        reqId: reqId, date: r[2], submitter: r[3],
                        submittedFor: r[1], status: r[4], reason: r[5] || '',
                        profile: profile, limits: limits
                    };
                    window.DADREQ_LIST.push(entry);
                    window.DADREQ_MAP[reqId] = {
                        requestStatus: r[4], requester: r[3], reason: r[5] || '',
                        profile: profile, limits: limits
                    };
                });
            }

            db.close();
        });
    });
})();
