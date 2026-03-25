// Shared DADREQ data loader — loads from req_signer via sql.js
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

            // Load Open requests from req_signer + req_signer_limit
            var openResults = db.exec(
                "SELECT o.id, o.req_date, o.submitter, o.gad_id, o.new_status, o.status_reason, " +
                "o.approver1_result, o.approver2_result, " +
                "l.id as lid, l.action, l.signer_limit_id, l.new_territory_id, l.new_policy_id, l.new_limit_amount, " +
                "l.new_approval_cc_id, l.new_exception, l.new_temp, l.new_temp_start_date, l.new_temp_end_date, l.new_business_rationale, l.new_business_control, " +
                "l.new_account_restriction, l.new_currency " +
                "FROM req_signer o LEFT JOIN req_signer_limit l ON l.req_signer_id = o.id ORDER BY o.id"
            );

            // Territory id -> code lookup
            var terrMap = {};
            var terrRes = db.exec("SELECT id, country_code FROM wd_territory");
            if (terrRes.length) terrRes[0].values.forEach(function(r) { terrMap[r[0]] = r[1]; });

            // Cost center id -> cc lookup
            var ccMap = {};
            var ccRes = db.exec("SELECT id, name FROM infor_cost_center");
            if (ccRes.length) ccRes[0].values.forEach(function(r) { ccMap[r[0]] = r[1]; });

            // Policy id -> category, system lookup
            var policyMap = {};
            var policyRes = db.exec("SELECT id, category, system FROM gdas_policy");
            if (policyRes.length) policyRes[0].values.forEach(function(r) { policyMap[r[0]] = { cat: r[1], sys: r[2] }; });

            // Group open limits by request id
            var openMap = {};
            if (openResults.length) {
                openResults[0].values.forEach(function(r) {
                    var reqNum = r[0];
                    if (!openMap[reqNum]) {
                        var reqStatusMap = { 1: 'Approved', 0: 'Rejected' };
                        var avpResultMap = { 1: 'Approved', 0: 'Rejected' };
                        openMap[reqNum] = {
                            id: reqNum, date: r[1], submitter: r[2], submittedFor: r[3],
                            status: reqStatusMap[r[4]] || 'Pending', reason: r[5] || '',
                            avpResult: avpResultMap[r[6]] || 'Pending',
                            tsaResult: avpResultMap[r[7]] || 'Pending',
                            limits: []
                        };
                    }
                    if (r[8] !== null) {
                        var actionMap = { 'Change': 'update', 'Remove': 'delete', 'Add': 'new', 'Unchange': 'nochange' };
                        var limEntry = { type: actionMap[r[9]] || r[9] };
                        if (r[10] !== null) limEntry.rowIndex = r[10];
                        if (r[9] === 'Change' || r[9] === 'Add') {
                            var amt = r[13] ? Number(r[13]).toLocaleString() : '0';
                            var pol = policyMap[r[12]] || {};
                            limEntry.newData = [
                                terrMap[r[11]] || '', pol.cat || '', amt, r[22] || '',
                                ccMap[r[14]] || '', r[15] ? 'Y' : 'N', r[16] ? 'Y' : 'N',
                                r[17] || '\u2014', r[18] || '\u2014',
                                r[19] ? 'Y' : 'N', r[20] ? 'Y' : 'N', pol.sys || '', r[21] || ''
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
                    reqId: reqId, id: o.id, date: o.date, submitter: o.submitter,
                    submittedFor: o.submittedFor, status: o.status, reason: o.reason,
                    avpResult: o.avpResult, tsaResult: o.tsaResult,
                    profile: {}, limits: o.limits
                };
                window.DADREQ_LIST.push(entry);
                window.DADREQ_MAP[reqId] = {
                    requestStatus: o.status, requester: o.submitter, reason: o.reason,
                    profile: {}, limits: o.limits
                };
            });

            db.close();
        });
    });
})();
