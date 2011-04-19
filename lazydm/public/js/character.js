(function($){
    Character = new Class({
  
        Implements: [Options, Events],
        options : {
            races : null
        },
        
        initialize: function (options) {
            this.setOptions(options);
            this.opt = this.options;
            this.opt.races = new Hash(this.opt.races);
            
            this.attrs = ['str','dex','wis','int','con','cha'];
            this.attrs.each(function (item) {
                this[item] = $(item);
            }, this);
            
            this.addEvent('recalc_stats', this.recalc_stats.bind(this));
            
            $('race').addEvent('change', this.update_race.bind(this));
        },
        
        transferStats: function (fromSelector) {
            var from = $$(fromSelector);
            
            this.attrs.each(function (item, index) {
                var base = this[item].getChildren('.base.stat')[0];
                base.set('html', from[index].get('html'));
            }, this);
            
            this.fireEvent('recalc_stats');
            window.diabox.hide();
        },
        
        update_race: function() { 
            var r = this.opt.races[$('race').value];
            
            this.attrs.each(function (item, index) {
                var stat = this[item].getChildren('.race.stat')[0];
                stat.set('html', (r.stat_mods[item] != 0) ? r.stat_mods[item] : "");
            }, this);
            
            this.fireEvent('recalc_stats');
        },
                        
        recalc_stats: function() {
            this.attrs.each(function (item) {
                var stats = this[item].getChildren('.stat');
                var total = stats[0];
                var sum = 0;
                var length = stats.length;
                for (i = 1; i < length; ++i) {
                    var n = stats[i].get('html').toInt();
                    if (!isNaN(n))
                        sum += stats[i].get('html').toInt();
                }    
                total.set('html', sum);
            }, this);
        },
        
        populate_races: function(selectarray) {
            if (this.opt.races == null) {
                
            }
            
            var books = $(selectarray[0]);
            var selected = books.getSelected().get('value');
            
            var races = $(selectarray[1]);
            races.empty();
            
            this.opt.races.each(function (item, index) {
                if (item.book.id == selected) {
                    races.adopt(new Element('option', { 
                        value: index,
                        html: item.name
                    }));
                }
            });
        },
    });
})(document.id || $);
