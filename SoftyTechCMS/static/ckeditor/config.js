/**
 * @license Copyright (c) 2003-2019, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see https://ckeditor.com/legal/ckeditor-oss-license
 */

CKEDITOR.editorConfig = function (config) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	//   config.uiColor = "#ff1100";
	config.extraPlugins = "youtube";
	config.extraPlugins = "filebrowser";
	// *NEEDS FIXING*
	config.extraPlugins = "slideshow";
	// config.extraPlugins = 'carousel'
	
	// config.filebrowserImageUploadUrl = '/filebrowser/';
};
