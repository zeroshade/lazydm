function addDelete(sUrl, sReplace) {            
    $$('button.delete').each(function(el) {
        el.addEvent('click', function(e) {
            e.stop();
            var row = el.getParent('div');
            var request = new Request({
                url: sUrl,
                link: 'chain',
                method: 'get',
                data: {
                    'delete': el.get('id').replace(sReplace,''),
                    ajax: 1
                },
                onRequest: function() {
                    new Fx.Tween(row, {
                        duration: 300
                    }).start('background-color', '#fb6c6c');
                },
                onSuccess: function() {
                    new Fx.Slide(row,{
                        duration: 400,
                        onComplete: function() {
                            row.dispose();
                        }
                    }).slideOut('vertical');
                },
                onFailure: function() {
                    new Fx.Tween(row, {
                        duration: 150
                    }).start('background-color','rgba(0,0,0,0)');
                    alert("FAILED");
                }
            }).send();
        });
    });
}
