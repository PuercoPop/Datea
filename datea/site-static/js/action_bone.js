


// DateaAction backbone model 
window.Datea.Action = Backbone.Model.extend();

// Action Collection
window.Datea.ActionCollection = Backbone.Collection.extend({
	model: Datea.Action,
	url: '/api/v1/action/',
});

window.Datea.CheckActionStats = function ($el, model) {
	// items
	if (model.get('item_count') == 1) {
		$('.item_count .singular', $el).show();
		$('.item_count .plural', $el).hide();
	}
	// comment
	if (model.get('comment_count') == 1) {
		$('.comment_count .singular', $el).show();
		$('.comment_count .plural', $el).hide();
	}
	// users
	if (model.get('user_count') == 1) {
		$('.user_count .singular', $el).show();
		$('.user_count .plural', $el).hide();
	}
}

// ACtion list item
window.Datea.ActionListItemView = Backbone.View.extend({
  
	tagName: 'div',
  
	className: 'action-item',

	render: function(){
  		this.$el.html(ich.action_list_item_tpl(this.model.toJSON()));
  
  		// follow widget
  		if (!Datea.my_user.isNew()) {
			this.follow_widget = new Datea.FollowWidgetView({
				object_type: 'dateaaction',
				object_id: this.model.get('id'),
				object_name: gettext('action'),
				followed_model: this.model,
				type: 'button',
				style: 'button-small', 
			});
			this.$el.find('.follow-button').html(this.follow_widget.render().el);
		}
      
		Datea.CheckActionStats(this.$el, this.model);
		return this;
  }
                                
});


// Action list view
window.Datea.ActionListView = Backbone.View.extend({
 
    tagName:'div',
    
    attributes: {
    	'class': 'actions',
    },
    
    events: {
    	'click .get-page': 'get_page',
    },
 
    initialize: function () {
    	this.model = new Datea.ActionCollection();
    	this.model.bind("reset", this.reset_event, this);
    	this.selected_mode = 'my_actions';
    	this.items_per_page = 10;
    	this.page = 0;
		this.pager_view = new Datea.PaginatorView({
			items_per_page: this.items_per_page,
			adjacent_pages: 1,
		});
    },
 
    render:function (ev) {
    	this.$el.html( ich.action_list_tpl());
    	this.build_filter_options();   	
    	this.fetch_actions();
    	
        return this;
    },
    
    // build filter options according to user
    build_filter_options: function () {
    	this.filter_options = [];
    	if (!Datea.my_user.isNew() && typeof(Datea.my_user_follows.find(function (f){ return f.get('object_type') == 'dateaaction'})) != 'undefined') {
    		
    		this.filter_options.push({value: 'my_actions', name: gettext('my actions')});
    		
    		if (this.model.find(function (action){
    				return action.get('user') == Datea.my_user.get('resource_uri');
    			})) {
    			this.filter_options.push({value: 'created_actions', name: gettext('actions created')});
    		}
    	}
    	this.filter_options.push({value: 'featured_actions', name: gettext('featured actions')});
        this.filter_options.push({value: 'all_actions', name: gettext('all actions')});
        
        // check availability of
        var self = this; 
        if (typeof(_.find(this.filter_options, function (op) {
        		return op.value == self.selected_mode;
        		})) == 'undefined') {
        	this.selected_mode = this.filter_options[0].value;
        }
    },
    
    render_filter: function() {
    	this.build_filter_options();
    	var self = this;
    	//console.log(this.selected_mode);
		this.action_filter = new Datea.DropdownSelect({
			options: this.filter_options,
			div_class: 'no-bg',
			init_value: this.selected_mode,
			callback: function (val) {
				self.selected_mode = val; 
				self.fetch_actions();
			}
		});
		this.$el.find('.filters').html(this.action_filter.render().el);
    },
    
    fetch_actions: function () {
    	if (this.selected_mode == 'my_actions' || this.selected_mode == 'created_actions') {
    		
    		var follows = Datea.my_user_follows.filter(function(fol){
	        	return fol.get('object_type') == 'dateaaction';
	        });
	        if (typeof(follows) != 'undefined' && follows.length > 0) {
	        	var ids = [];
	        	for (i in follows) {
	        		ids.push(follows[i].get('object_id'));
	        	}
	        	this.model.fetch({
	        		data: {'id__in': ids.join(',')}
	        	})	
	        }
    	
    	}else if (this.selected_mode == 'featured_actions') {
    		this.model.fetch({
    			data: {featured: 1, orderby: '-created'}
    		});
    		
    	}else if (this.selected_mode == 'all_actions'){
    		this.model.fetch({ data: {orderby: '-created'} });
    	}
    },
    
    filter_items: function () {
    	
    	if (this.selected_mode == 'my_actions') {
    		this.render_actions = this.model.models;
        
        }else if (this.selected_mode == 'created_actions') {
        	this.render_actions = this.model.filter(function(action) { return action.get('user') == Datea.my_user.get('resource_uri') });	
        
        }else if (this.selected_mode == 'featured_actions')  {
        	this.render_actions = this.model.filter(function(action) { return action.get('featured')});	
        
        }else if (this.selected_mode == 'all_actions')  {
        	this.render_actions = this.model.models;	
        }  
    },
      
    render_page: function(page) {
    	var $list = this.$el.find('#action-list');
    	$list.empty();
    	
    	if (typeof(page) != 'undefined') {
    		this.page = page;
    	}
    	
    	var add_pager = false;
    	if (this.render_actions.length > this.items_per_page) {
    		var items = _.rest(this.render_actions, this.items_per_page*this.page);
       		items = _.first(items, this.items_per_page);
       		add_pager = true;  
    	}else{
    		items = this.render_actions;
    	}
    	
    	_.each(items, function (item) {
            	$list.append(new Datea.ActionListItemView({model:item}).render().el);
        }, this);
        
        var $pager_div = this.$el.find('.action-pager');
		if (add_pager) {
			$pager_div.html( this.pager_view.render_for_page(this.page,this.render_actions.length).el);
			$pager_div.removeClass('hide');
		}else{
			$pager_div.addClass('hide');
		}
    },
    
    get_page: function(ev) {
    	ev.preventDefault();
		this.render_page(parseInt(ev.target.dataset.page));
		this.$el.find('.scroll-area').scrollTop(0);
    },
    
    reset_event: function(ev) {
    	this.render_filter();
    	this.filter_items();
    	this.render_page(0);
    }
    
});


// Start action view -> create new action
window.Datea.ActionStartView = Backbone.View.extend({
	
	tagName: 'div',
	
	render: function(eventName) {
		this.$el.html( ich.fix_base_content_single_tpl({'class': 'dotted-bg'}));
		this.$el.find('#content').html( ich.action_create_tpl());
		return this;	
	}
	
});






