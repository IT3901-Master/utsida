$(function () {
    $('#world-map').vectorMap({
        map: 'world_mill',
        zoomOnScroll: false,
        series: {
            regions: [{
                values: country_code_data,
                scale: ['#cceeff', '#0077b3']
            }]
        },
        onRegionTipShow: function(e, el, code) {
            if (country_code_data[code] == undefined)
                el.html(el.html()+ " (Ingen registrerte utveklsinger)" );
            else
                el.html(el.html()+ ' (' + country_code_data[code]+ ' utveklsinger)');
        }
    });
});



