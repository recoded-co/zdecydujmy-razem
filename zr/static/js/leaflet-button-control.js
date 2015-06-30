/**
 * Created by marcinra on 6/27/14.
 */
L.Control.Button = L.Control.extend({
options: {
    position: 'topright'
},
initialize: function (options) {
    this._button = {};
    this.setButton(options);
},

onAdd: function (map) {
    this._map = map;
    var container = L.DomUtil.create('div', 'leaflet-control-button');
    this._container = container;
    this._update();
    return this._container;
},

onRemove: function (map) {
},

setButton: function (options) {
    var button = {
    'text': options.text, //string
    'iconUrl': options.iconUrl, //string
    'onClick': options.onClick, //callback function
    'hideText': !!options.hideText, //forced bool
    'maxWidth': options.maxWidth || 70, //number
    'doToggle': options.toggle,	//bool
    'toggleStatus': false	//bool
    };

    this._button = button;
    this._update();
},
getText: function () {
    return this._button.text;
},
getIconUrl: function () {
    return this._button.iconUrl;
},
destroy: function () {
    this._button = {};
    this._update();
},
toggle: function (e) {
    if(typeof e === 'boolean'){
    this._button.toggleStatus = e;
    }
    else{
    this._button.toggleStatus = !this._button.toggleStatus;
    }
    this._update();
},
_update: function () {
    if (!this._map) {
    return;
    }

    this._container.innerHTML = '';
    this._makeButton(this._button);
},

_makeButton: function (button) {
    var link = L.DomUtil.create('a', 'leaflet-control-info', this._container);
        link.href = '#';
        link.title = 'Szczegóły o MPZP';

    if(button.toggleStatus)
        L.DomUtil.addClass(link,'leaflet-buttons-control-toggleon');

    L.DomEvent
        .on(link, 'click', L.DomEvent.stopPropagation)
        .on(link, 'click', L.DomEvent.preventDefault)
        .on(link, 'click', button.onClick, this)
        .on(link, 'click', this._clicked, this)
        .on(link, 'dblclick', L.DomEvent.stopPropagation);

    return link;

    // var newButton = L.DomUtil.create('div', 'leaflet-buttons-control-button', this._container);
    // if(button.toggleStatus)
    // L.DomUtil.addClass(newButton,'leaflet-buttons-control-toggleon');

    // L.DomEvent
    // .addListener(newButton, 'click', L.DomEvent.stop)
    // .addListener(newButton, 'click', button.onClick,this)
    // .addListener(newButton, 'click', this._clicked,this);
    // L.DomEvent.disableClickPropagation(newButton);
    // return newButton;

},
_clicked: function () { //'this' refers to button
    if(this._button.doToggle){
        if(this._button.toggleStatus) {	//currently true, remove class
            L.DomUtil.removeClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
        else{
            L.DomUtil.addClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
    this.toggle();
    }
    return;
    }

});


L.Control.Help = L.Control.extend({
options: {
    position: 'topright'
},
initialize: function (options) {
    this._button = {};
    this.setButton(options);
},

onAdd: function (map) {
    this._map = map;
    var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
    this._container = container;
    this._update();
    return this._container;
},

onRemove: function (map) {
},

setButton: function (options) {
    var button = {
    'text': options.text, //string
    'iconUrl': options.iconUrl, //string
    'onClick': options.onClick, //callback function
    'hideText': !!options.hideText, //forced bool
    'maxWidth': options.maxWidth || 70, //number
    'doToggle': options.toggle, //bool
    'toggleStatus': false   //bool
    };

    this._button = button;
    this._update();
},
getText: function () {
    return this._button.text;
},
getIconUrl: function () {
    return this._button.iconUrl;
},
destroy: function () {
    this._button = {};
    this._update();
},
toggle: function (e) {
    if(typeof e === 'boolean'){
    this._button.toggleStatus = e;
    }
    else{
    this._button.toggleStatus = !this._button.toggleStatus;
    }
    this._update();
},
_update: function () {
    if (!this._map) {
    return;
    }

    this._container.innerHTML = '';
    this._makeButton(this._button);
},

_makeButton: function (button) {
    var link = L.DomUtil.create('a', 'leaflet-control-help', this._container);
        link.href = '#';
        link.title = 'Pomoc';

    L.DomEvent
        .on(link, 'click', L.DomEvent.stopPropagation)
        .on(link, 'click', L.DomEvent.preventDefault)
        .on(link, 'click', button.onClick,this)
        .on(link, 'dblclick', L.DomEvent.stopPropagation);

    return link;
},
_clicked: function () { //'this' refers to button
    if(this._button.doToggle){
        if(this._button.toggleStatus) { //currently true, remove class
            L.DomUtil.removeClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
        else{
            L.DomUtil.addClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
    this.toggle();
    }
    return;
    }

});


L.Control.Doc = L.Control.extend({
options: {
    position: 'topright'
},
initialize: function (options) {
    this._button = {};
    this.setButton(options);
},

onAdd: function (map) {
    this._map = map;
    var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
    this._container = container;
    this._update();
    return this._container;
},

onRemove: function (map) {
},

setButton: function (options) {
    var button = {
    'text': options.text, //string
    'iconUrl': options.iconUrl, //string
    'onClick': options.onClick, //callback function
    'hideText': !!options.hideText, //forced bool
    'maxWidth': options.maxWidth || 70, //number
    'doToggle': options.toggle, //bool
    'toggleStatus': false   //bool
    };

    this._button = button;
    this._update();
},
getText: function () {
    return this._button.text;
},
getIconUrl: function () {
    return this._button.iconUrl;
},
destroy: function () {
    this._button = {};
    this._update();
},
toggle: function (e) {
    if(typeof e === 'boolean'){
    this._button.toggleStatus = e;
    }
    else{
    this._button.toggleStatus = !this._button.toggleStatus;
    }
    this._update();
},
_update: function () {
    if (!this._map) {
    return;
    }

    this._container.innerHTML = '';
    this._makeButton(this._button);
},

_makeButton: function (button) {
    var link = L.DomUtil.create('a', 'leaflet-control-doc', this._container);
        link.href = '#';
        link.title = 'Dokumentacja';

    L.DomEvent
        .on(link, 'click', L.DomEvent.stopPropagation)
        .on(link, 'click', L.DomEvent.preventDefault)
        .on(link, 'click', button.onClick,this)
        .on(link, 'dblclick', L.DomEvent.stopPropagation);

    return link;
},
_clicked: function () { //'this' refers to button
    if(this._button.doToggle){
        if(this._button.toggleStatus) { //currently true, remove class
            L.DomUtil.removeClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
        else{
            L.DomUtil.addClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
    this.toggle();
    }
    return;
    }

});
