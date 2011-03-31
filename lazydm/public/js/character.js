(function($){
    Character = new Class({
  
        Implements: [Options, Events],
        options : {
        },
        
        initialize: function (options) {
            this.setOptions(options);
            this.opt = this.options;
            
            this.attrs = ['str','dex','wis','int','con','cha'];
            this.attrs.each(function (item) {
                this[item] = $(item);
            }, this);
            
            this.addEvent('recalc_stats', this.recalc_stats.bind(this));
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
        
        recalc_stats: function() {
            this.attrs.each(function (item) {
                var stats = this[item].getChildren('.stat');
                var total = stats[0];
                var sum = 0;
                var length = stats.length;
                for (i = 1; i < length; ++i)
                    sum += stats[i].get('html').toInt();
                    
                total.set('html', sum);
            }, this);
        },
    });
})(document.id || $);
