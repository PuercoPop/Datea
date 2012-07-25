hardcode_map_id = 1;

// Main App Router for the Datea Plattform in the client
Datea.AppRouter = Backbone.Router.extend({
 
    routes:{
        "":"home",
        "_=_": "fb_login_redirect",
        "action/start": "action_start",
        "action/create/:action_type": "action_create",
        
        "mapping/:map_id": 'open_mapping_tab',
        "mapping/:map_id/edit": 'open_mapping_edit',
        "mapping/:map_id/admin": 'open_mapping_admin',
        "mapping/:map_id/:tab_id": 'open_mapping_tab',
        "mapping/:map_id/reports/item:report_id": 'open_mapping_item',
       	"mapping/:map_id/:tab_id/:method_id": 'open_mapping_tab',
    },
 
    home:function () {
    	//this.open_mapping_tab(hardcode_map_id);
    	//return;
    	clear_admin_controls();
    	this.my_profile_home_view = new Datea.MyProfileHomeView({model:Datea.my_user});
        $('#main-content-view').html(this.my_profile_home_view.render().el);
    },
    
    fb_login_redirect:function () {
    	clear_admin_controls();
    	this.navigate('/');
    },
    
    // new action homeview -> select which action type to create
    action_start: function () {
    	clear_admin_controls();
    	$('#main-content-view').html(new Datea.ActionStartView().render().el);
    },
    
    // create new action (mapping or whatever)
    action_create: function (action_type) {
    	clear_admin_controls();
    	if (action_type == 'mapping') {
			$('#main-content-view').html( ich.fix_base_content_single_tpl());
    		this.mapping = new Datea.MappingFormView({model: new Datea.Mapping()});
    		$('#content').html(this.mapping.render().el);
    		this.mapping.attach_map();
    	}	
    },
    
    // open a mapping tab on the mapping action
    open_mapping_tab: function(map_id, tab_id, method_id) {
    	
    	var params = {
    		tab_id: tab_id,
			method_id: method_id,
    	}

    	// checkif mapping already exists (not drawing everything again!)
    	if (this.mapping_view && this.mapping_view.model.get('id') == map_id) {
    		// test if layout rendered
    		if ($('#mapping-'+map_id).size() == 0) {
    			this.mapping_view.render();
    		}
    		this.mapping_view.render_tab(params);
    		
    	}else{
    		var self = this;
    		clear_admin_controls();
    		this.build_mapping_main_view(map_id, function () {
    			self.mapping_view.render_tab(params);
    		});
    	}
    },
    
    // open a single map item in detail view
    open_mapping_item: function(map_id, item_id) {

    	var params = {
    		tab_id: 'reports',
			item_id: item_id,
    	}
    	// check if mapping already exists (not drawing everything again!)
    	if (this.mapping_view && this.mapping_view.model.get('id') == map_id) {
    		// test if layout rendered
    		if ($('#mapping-'+map_id).size() == 0) {
    			this.mapping_view.render();
    		}
    		this.mapping_view.render_item(params);
    	}else{
    		var self = this;
    		clear_admin_controls();
    		this.build_mapping_main_view(map_id, function () {
    			self.mapping_view.render_item(params);
    		})
    	}
    },
    
        
    fetch_mapping_data: function (map_id, callback) {
    	var self = this;
    	this.mapping_model = new Datea.Mapping({id: map_id});
    	this.map_items = new Datea.MapItemCollection();
    	this.mapping_model.fetch({
    		success: function () {
    			callback();
    		},
    	});
    },
    
    // Build mapping and add it to the dom
    build_mapping_main_view: function(map_id, callback) {
    	var self = this;
    	this.fetch_mapping_data(map_id, function(){
			self.mapping_view = new Datea.MappingMainView({
				el: $('#main-content-view'),
				model: self.mapping_model,
				map_items: self.map_items,
			});
			self.mapping_view.render();
			self.map_items.fetch({
				data: {'action': map_id, 'order_by': '-created'},
				success: function ( ) {
					if (typeof(callback) != 'undefined') {
						callback();
					}
				}
			});
		});
    },
    
    // Build mapping admin view and addit to the dom
    build_mapping_admin_view: function(map_id, callback) {
    	var self = this;
    	this.fetch_mapping_data(map_id, function(){
			self.mapping_admin_view = new Datea.MappingAdminView({
				el: $('#main-content-view'),
				model: self.mapping_model,
				map_items: self.map_items,
			});
			self.map_items.fetch({
				data: {'action': map_id, 'order_by': '-created'},
				success: function ( ) {
					self.mapping_admin_view.render();
					if (typeof(callback) != 'undefined') {
						callback();
					}
				}
			});
		});
    },
    
    // Build mapping EDIT view and addit to the dom
    build_mapping_edit_view: function(map_id, callback) {
    	var self = this;
    	this.fetch_mapping_data(map_id, function(){
			self.mapping_edit_view = new Datea.MappingFormView({
				el: $('#main-content-view'),
				model: self.mapping_model,
			});
			if (typeof(callback) != 'undefined') {
				callback();
			}
		});
    },
    
    open_mapping_edit: function(map_id) {
    	// check if mapping already exists
    	if (this.mapping_model && this.mapping_model.get('id') == map_id) {
    		// edit view created
    		if (this.mapping_edit_view) {
    			this.mapping_edit_view.render();
    		}else{
    			this.mapping_edit_view = new Datea.MappingFormView({
    				el: $('#main-content-view'),
    				model: this.mapping_model,
    			});
    			this.mapping_edit_view.render();
    		}
    		
    	}else{
    		var self = this;
    		clear_admin_controls();
    		this.build_mapping_edit_view(map_id, function () {
    			self.mapping_edit_view.render();
    		})
    	}
    },

    open_mapping_admin: function(map_id) {
    	// check if mapping already exists
    	if (this.mapping_model && this.map_items && this.mapping_model.get('id') == map_id) {
    		// admin view created
    		if (this.mapping_admin_view) {
    			this.mapping_admin_view.render();
    		}else{
    			this.mapping_admin_view = new Datea.MappingAdminView({
    				el: $('#main-content-view'),
    				model: this.mapping_model,
    				map_items: this.map_items,
    			});
    			this.mapping_admin_view.render();
    			
    		}
    		
    	}else{
    		var self = this;
    		clear_admin_controls();
    		this.build_mapping_admin_view(map_id, function () {
    			self.mapping_admin_view.render();
    		})
    	}
    }, 
});

function clear_admin_controls() {
	$('#setting-controls').empty();
}
