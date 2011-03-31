/*
 * 
 * Provides the following functions:
 *      dragdice -- mousedown event handler for moving dice groups around
 *      custom_parse
 * 
 * 
 */
    
    function turnDiceOn(elem, title, fn) {
        elem.removeClass('empty').addClass('full').addEvent('mousedown', fn);
        elem.set('title', title);
    }
    
    function turnDiceOff(elem,fn) {
        elem.empty().removeClass('full').addClass('empty').removeEvent('mousedown',fn);
        elem.set('title',null);
        elem.eliminate('title');
    }
    
    function dragdice(event) {
        event.stop();
        var dieset = this;
        var clone = dieset.clone().setStyles(dieset.getCoordinates()).setStyles({
           opacity: 0.7,
           position: 'absolute',
           'z-index': 9999,
           width: '256px',
           display: 'block'
        }).inject(document.body);
       
        var drag = new Drag.Move(clone, {
            precalculate: true,
            container: $('diabox_content'),
            droppables: $$('li.dieholder.empty'),
            
            onDrop: function (dragging, location) {
                if (location) {
                    turnDiceOn(location, dragging.get('title'), dragdice);
                    var prev = location.getPrevious('.attr');
                    if (prev != null)
                        prev.getChildren('.stat')[0].set('html', dragging.get('title'));
                    
                    prev = dieset.getPrevious('.attr');
                    if (prev != null)
                        prev.getChildren('.stat')[0].set('html', '');
                    
                    turnDiceOff(dieset, dragdice);
                }
                dragging.destroy();
            },
            onEnter: function (dragging, location) {
               location.adopt(dragging.clone().setStyles(dragging.getCoordinates()).setStyles({
                   position: 'asolute'
               }).getChildren());
            },
            onLeave: function (dragging, location) {
               location.empty();
            },
        });
        drag.start(event);
    }
    
    function addToDiceBox(dice) {
        $$('li.dieholder.full').each(function (item) {
            turnDiceOff(item, dragdice);
        });
        $$('#attrs_box li.attr .stat').each(function (item) {
            var html = item.get('html');
            item.set('html', '');
        });
        var idx = 0;
        $$('#dicebox_box li.dieholder').each(function (item) {
            var min = null;
            var minval = 7;
            var sum = 0;
            for ( i = 0; i < 4; ++i, ++idx) {
                var span = new Element('span', { class: "die_6_" + dice[idx], html: "&nbsp;" });
                span.inject(item);
                sum += dice[idx];
                if (dice[idx] < minval) {
                    minval = dice[idx];
                    min = span;
                }
            }
            sum -= minval;
            min.addClass('dropdie');
            turnDiceOn(item, sum, dragdice)
        });
    }
