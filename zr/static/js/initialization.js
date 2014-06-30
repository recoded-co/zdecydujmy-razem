/**
 * Created by marcinra on 11/9/13.
 */

var appConfiguration = function() {
    var appPlanId='1';
    var appAuthor='626';
    return {
        setAuthor: function(authorId){
            appAuthor=authorId;
        },
        getAuthor: function() {
            return appAuthor;
        },
        setPlanId: function(temp){
            appPlanId = temp;
        },
        getPlanId: function(){
            return appPlanId;
        }
    }
}
var configuration = appConfiguration();


function page_init(){
        var post_box = document.getElementById("resizible_jquery");
        var map_box = document.getElementById("mapsquare");
        var absolut_width = parseInt(document.getElementById("row_box").offsetWidth);
        post_box.style.width = "{{ configuration.default }}%";
        //map_box.style.width = ""+(99 - parseInt("{{ configuration.default }}") - parseInt((margin_gap*100)/absolut_width))+"%";
        //middle_background
        if( "{{ configuration.side|dirparser }}"=="left"){
            $('.ui-resizable-e').addClass('middle_background');
        } else {
            $('.ui-resizable-w').addClass('middle_background');
        }
        calibration();
}

function resize() {
        var body = document.getElementsByTagName("body")[0];
        window.doc = document.getElementsByTagName("body")[0];
        calibration();

        var post_box = document.getElementById("resizible_jquery");
        var map_box = document.getElementById("mapsquare");
        var middle_man = document.getElementById("middleman");
        var dashbord_map = document.getElementById("row_box");


        post_box.style.left = "0px";
        if( "{{ configuration.side|dirparser }}"=="left"){
            map_box.style.width = ""+(dashbord_map.offsetWidth - post_box.offsetWidth -1)+"px";
        } else {
            map_box.style.width = ""+(dashbord_map.offsetWidth - post_box.offsetWidth -1)+"px";
        }
    }

function calibration() {
    var body = document.getElementsByTagName("body")[0];

        if (typeof window.innerWidth != 'undefined') {
            viewportwidth = window.innerWidth,
            viewportheight = window.innerHeight
        }
        else if (typeof document.documentElement != 'undefined' && typeof document.documentElement.clientWidth != 'undefined' && document.documentElement.clientWidth != 0) {
            viewportwidth = document.documentElement.clientWidth,
            viewportheight = document.documentElement.clientHeight
        }
        else {
            viewportwidth = document.getElementsByTagName('body')[0].clientWidth,
            viewportheight = document.getElementsByTagName('body')[0].clientHeight
        }
        body.style.width = viewportwidth+"px";
        body.style.height = viewportheight+"px";
}