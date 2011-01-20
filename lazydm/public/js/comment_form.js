window.addEvent('domready', function() {
    var comform = document.id('comment-form');
    new Form.Validator.Inline(comform);
    new Form.Request(comform, 'comment-form-section', {
        extraData: {
            'partial': 'true'
        }
    });
});

