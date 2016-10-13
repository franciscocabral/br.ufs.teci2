var express = require('express');
var router = express.Router();

/* GET reminder listing. */
router.get('/', function(req, res, next) {
    res.send({teste:1243});
});

module.exports = router;
