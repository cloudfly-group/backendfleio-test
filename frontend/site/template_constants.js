// Global end-user panel configuration

'use strict';

var user_config = {
  api_url: 'http://localhost:8000/api',
  language: 'en', // default language
  base_url: '/',
  home_url: '/',
  // logo_light: 'https://fleio.com/images/logo.png',
  // logo_dark: 'https://fleio.com/images/logo.png',
  // shutdown_instance_note: "NOTE: The instance will continue to be charged even if it's shutdown. Delete the instance if you want to no longer be charged.",
  // toast_hide_delay: 3000, // bottom-left toast message animation delay in milliseconds
  items_display_mode: 'cardview', //cardview || listview
  enable_debug: false,  // set to true in development to enable angular debug
  flavors_as_cards: false, // used on instance creation for flavors selector layout
  local_compute_storage_enabled: true, // used on instance create on boot source selection
  preselect_public_networks: true, // preselects networks with public tag on instance creation form
  hide_networks_if_only_one_available: true, // if there is only one network available on the instance creation form, preselect it and hide the input field
  show_root_password_field_on_new_instance_form: true,
  root_password_mandatory_on_new_instance_form: false,
  show_userdata_on_new_instance_form: true,
  customThemesCallback: function(mdThemingProvider) {
    // read the docs on how to define new themes
  },
  registeredThemes: ['Spring', 'Navy', 'Dusk'], // list of themes that can be used by a user
  new_object_arrow_img_source: 'images/arrow.png',
};

try {
  angular.module('fleio.config').constant('CONFIG', user_config);
}
catch (err) {
  angular.module('fleiostaff.config').constant('USER_CONFIG', user_config);
}
