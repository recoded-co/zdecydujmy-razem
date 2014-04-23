L.Control.MeasurePolygon = L.Control.extend({
	options: {
		position: 'topright'
	},

	onAdd: function (map) {

		var className = 'leaflet-bar leaflet-control',
		    container = L.DomUtil.create('div', className);

		this._createButton('', 'Pomiar obszaru', 'leaflet-control-measure leaflet-bar-part leaflet-bar-part-top-and-bottom', container, this._toggleMeasure, this);

		return container;
	},

	_createButton: function (html, title, className, container, fn, context) {
		var link = L.DomUtil.create('a', 'leaflet-control-measure', container);
		link.innerHTML = html;
		link.href = '#';
		link.title = title;

		L.DomEvent
			.on(link, 'click', L.DomEvent.stopPropagation)
			.on(link, 'click', L.DomEvent.preventDefault)
			.on(link, 'click', fn, context)
			.on(link, 'dblclick', L.DomEvent.stopPropagation);

		return link;
	},

	_toggleMeasure: function () {
        console.log('Polygon');
		this._measuring = !this._measuring;
        //check remote switcher in case that other control is still on
        this._map.remoteControlSwitchOff();

        if(this._measuring) {

            //arm remote switcher
            this._map.setRemoteControlSwitch(this,this._remoteSwitchOff);

			L.DomUtil.addClass(this._container, 'leaflet-control-measure-on');
			this._startMeasuring();
		} else {
			L.DomUtil.removeClass(this._container, 'leaflet-control-measure-on');
			this._stopMeasuring();
		}
	},
    _remoteSwitchOff: function() {
        L.DomUtil.removeClass(this._container, 'leaflet-control-measure-on');
		this._stopMeasuring();
    },
	_startMeasuring: function() {
		this._oldCursor = this._map._container.style.cursor;
		this._map._container.style.cursor = 'crosshair';

        if(!this._areaPoints){
            this._areaPoints = new Array();
        }

		this._doubleClickZoom = this._map.doubleClickZoom.enabled();
		this._map.doubleClickZoom.disable();

		L.DomEvent
			.on(this._map, 'mousemove', this._mouseMove, this)
			.on(this._map, 'click', this._mouseClick, this)
			.on(this._map, 'dblclick', this._finishPath, this);
			//.on(document, 'keydown', this._onKeyDown, this);

		if(!this._layerPaint) {
			this._layerPaint = L.layerGroup().addTo(this._map);	
		}
	},

	_stopMeasuring: function() {
		this._map._container.style.cursor = this._oldCursor;

		L.DomEvent
			.off(this._map, 'mousemove', this._mouseMove, this)
			.off(this._map, 'click', this._mouseClick, this)
			.off(this._map, 'dblclick', this._mouseClick, this);

		if(this._doubleClickZoom) {
			this._map.doubleClickZoom.enable();
		}

		if(this._layerPaint) {
			this._layerPaint.clearLayers();
		}
		
		this._restartPath();
	},

	_mouseMove: function(e) {
		if(!e.latlng || !this._lastPoint) {
			return;
		}
		
		if(!this._layerPaintPathTemp) {
			this._layerPaintPathTemp = L.polyline([this._lastPoint, e.latlng], { 
				color: 'black',
				weight: 1.5,
				clickable: false,
				dashArray: '6,3'
			}).addTo(this._layerPaint);
		} else {
			this._layerPaintPathTemp.spliceLatLngs(0, 2, this._lastPoint, e.latlng);
		}

        if(this._tooltip) {
			this._updatePosition(e.latlng);
        }
	},

	_mouseClick: function(e) {
		// Skip if no coordinates
		if(!e.latlng) {
			return;
		}
        this._lastPositionAdded = e.latlng;
        this._areaPoints.push(e.latlng);

		// If this is already the second click, add the location to the fix path (create one first if we don't have one)
		if(this._lastPoint && !this._layerPaintPath) {
			this._layerPaintPath = L.polygon([this._lastPoint], {
				color: 'black',
				weight: 2,
				clickable: true
			}).addTo(this._layerPaint);
		}

		if(this._layerPaintPath) {
			this._layerPaintPath.addLatLng(e.latlng);
		}

        if(!this._tooltip){
            this._createTooltip(e.latlng);
            var text = '<div class="leaflet-measure-tooltip-message">Kliknij, aby kontynuować rysowanie. Kliknij podwójnie, aby zamknąć obszar.</div>';
		    this._tooltip._icon.innerHTML = text;
        }
		// Upate the end marker to the current location
		if(this._lastCircle) {
			this._layerPaint.removeLayer(this._lastCircle);
		}

		this._lastCircle = new L.CircleMarker(e.latlng, { 
			color: 'black', 
			opacity: 1, 
			weight: 1, 
			fill: true, 
			fillOpacity: 1,
			radius:2,
			clickable:true
		}).addTo(this._layerPaint);
		
		this._lastCircle.on('click', function() { this._finishPath(); }, this);

		// Save current location as last location
		this._lastPoint = e.latlng;
	},

	_finishPath: function(e) {
        if(this._areaPoints && this._areaPoints.length>2){
            this._updateTooltipPosition();
            this._updateTooltipDistance();
        }
		// Remove the last end marker as well as the last (moving tooltip)
		if(this._lastCircle) {
			this._layerPaint.removeLayer(this._lastCircle);
		}
		if(this._layerPaint && this._layerPaintPathTemp) {
			this._layerPaint.removeLayer(this._layerPaintPathTemp);
		}

		// Reset everything
		this._restartPath();
	},

	_restartPath: function() {
		this._distance = 0;
		this._tooltip = undefined;
		this._lastCircle = undefined;
		this._lastPoint = undefined;
		this._layerPaintPath = undefined;
		this._layerPaintPathTemp = undefined;
        this._lastPositionAdded = undefined;
        this._areaPoints = new Array();;
	},
	
	_createTooltip: function(position) {
        if(position === undefined){
            position = this._lastPositionAdded;
        }
		var icon = L.divIcon({
			className: 'leaflet-measure-tooltip',
			iconAnchor: [-5, -5]
		});
		this._tooltip = L.marker(position, { 
			icon: icon,
			clickable: false
		}).addTo(this._layerPaint);
        //this._updateTooltipPosition();
        //this._updateTooltipDistance();
	},

	_updateTooltipPosition: function() {
		this._tooltip.setLatLng(this._lastPositionAdded);
	},
    _updatePosition: function(position) {
		this._tooltip.setLatLng(position);
	},

	_updateTooltipDistance: function() {

        var totalRound = this._polygonArea(this._areaPoints);
        //console.log(this._areaPoints);
        //console.log("" + totalRound);
        var text ="";
        //TODO: Fix intersection
        //if(this._layerPaintPath.intersects()){
        //    text = '<div class="leaflet-measure-tooltip-total">Niepoprawny wielokąt</div>';
        //}else {
            text = '<div class="leaflet-measure-tooltip-total">' + totalRound + '</div>';
        //}
		this._tooltip._icon.innerHTML = text;
	},
    _polygonArea: function(list){

		var area = L.GeometryUtil.geodesicArea(list);
        return L.GeometryUtil.readableArea(area, true);
        }
});

L.Map.mergeOptions({
	measurePolygonControl: false
});

L.Map.addInitHook(function () {
	if (this.options.measurePolygonControl) {
		this.measurePolygonControl = new L.Control.MeasurePolygon();
		this.addControl(this.measurePolygonControl);
	}
});

L.control.measurePolygon = function (options) {
	return new L.Control.MeasurePolygon(options);
};
