// Shared dummy DADREQ data loader — loads db/dadreq.db via sql.js and exposes:
//   window.DADREQ_LIST  — array of all entries
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
            var results = db.exec('SELECT reqId, date, submitter, submittedFor, status, reason, profile, limits FROM dadreq ORDER BY reqId');
            db.close();

            if (!results.length) return;
            var rows = results[0].values;
            rows.forEach(function(r) {
                var profile = JSON.parse(r[6] || '{}');
                var limits  = JSON.parse(r[7] || '[]');
                var entry = {
                    reqId:        r[0],
                    date:         r[1],
                    submitter:    r[2],
                    submittedFor: r[3],
                    status:       r[4],
                    reason:       r[5],
                    profile:      profile,
                    limits:       limits
                };
                window.DADREQ_LIST.push(entry);
                window.DADREQ_MAP[entry.reqId] = {
                    requestStatus: entry.status,
                    requester:     entry.submitter,
                    reason:        entry.reason,
                    profile:       profile,
                    limits:        limits
                };
            });
        });
    });
})();
