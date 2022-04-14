function getPosition() {
    return new Promise((res, rej) => {
        navigator.geolocation.getCurrentPosition(res, rej);
    });
}

function main() {
    getPosition().then(resp => {
        const lat = resp.coords.latitude;
        const lon = resp.coords.longitude;
        console.log(lat, lon)
        
        var map1 = L.map('map1').setView([lat, lon], 15);

        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 18,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: 'pk.eyJ1Ijoic2hhYWRlbnNzIiwiYSI6ImNrem0wbG41YjJkc3Qyd24yeGl2MTlkdXYifQ.6QUloRYZssJlCCzbwsXmgQ'
        }).addTo(map1);

        var geocodeService = L.esri.Geocoding.geocodeService()
        geocodeService.reverse()
            .latlng([lat, lon])
            .run(function (error, result) {
                if (error) {
                return;
            }
            const myLoc = document.getElementById("myLoc");
            myLoc.textContent = result.address.Match_addr
            L.marker(result.latlng).addTo(map1);
        });

        // map.on('click', function (e) {
        //     geocodeService.reverse().latlng(e.latlng).run(function (error, result) {
        //     console.log(e.latlng)
        //         if (error) {
        //         return;
        //     }
        //     L.marker(result.latlng).addTo(map).bindPopup(result.address.Match_addr).openPopup();
        //     });
        // });
    });
}

main();