// Define the map
//const map = L.map('map', { attributionControl: false }).setView([51.480, -0.13], 13); // Set your initial coordinates and zoom level
// Add the image overlay layer with adjusted bounds for increased width
//const imageUrl = '/livingarchive/static/assets/img/Guwak.jpg';
//const imageBounds = [[51.53, -0.20], [51.4, -0.05]]; // Adjust the bounds for increased width
//L.imageOverlay(imageUrl, imageBounds).addTo(map);
            var string = ""
            string = "{% for post in posts %}{{ post.title }}@*&!{% endfor %}";
            var title = string.split("@*&!");

            string = "{% for post in posts %}{{ post.address }}@*&!{% endfor %}";
            var address = string.split("@*&!");
            console.info(address)

            string = "{% for post in posts %}{{ post.intro }}@*&!{% endfor %}";
            var intro = string.split("@*&!");

            string = "{% for post in posts %}{{ post.body }}@*&!{% endfor %}";
            var body = string.split("@*&!");

            string = "{% for post in posts %}{{ post.url }}@*&!{% endfor %}";
            var url = string.split("@*&!");

            string = "{% for post in posts %}{{ post.owner.id }}@*&!{% endfor %}";
            var uids = string.split("@*&!");

            string = "{% for post in posts %}{% image post.image fill-200x150 as blog_img %}{{blog_img.url}}@*&!{% endfor %}";
            var imgs = string.split("@*&!");

            var blogSet = {}
            for (let i = 0; i < uids.length; i++) {
                const uid = uids[i]
                if (uid === '') continue
                if (typeof (blogSet[uid]) === 'undefined') blogSet[uid] = []
                blogSet[uid].push([title[i], address[i], i, intro[i], body[i], url[i], imgs[i], uid])
            }

            var map = L.map('map', {attributionControl: false}).setView(-23.3000384, 134.0782539], 5);

            L.tileLayer('http://{s}.google.com/vt/lyrs=m&x={x}&y={y}&z={z}', {
                maxZoom: 20,
                subdomains: ['mt0', 'mt1', 'mt2', 'mt3']
            }).addTo(map);

            L.Control.geocoder().addTo(map);

            // add overlay
            const imageUrl = "{% static 'assets/img/overlay.png' %}";
            var imageBounds = [[-8.901186, 128.0], [-28.177350, 138.9]];
            L.imageOverlay(imageUrl, imageBounds).addTo(map);
            L.imageOverlay(imageUrl, imageBounds).bringToFront();

           let markerSet = []

            var myMarkerClusterGroup = L.markerClusterGroup()

            var colorSet = ['#F79327', '#DB005B', '#FF55BB', '#FFD3A3', '#FCFFB2', '#B6EAFA', '#B2A4FF', '#FF6969', '#B4FF9F']

            let index = 0
            for (const uid in blogSet) {
                if (Object.hasOwnProperty.call(blogSet, uid)) {
                    const locations = blogSet[uid];
                    const pointList = []

                    for (i = 0; i < locations.length; i++) {
                        const l = locations[i][1].split(",");
                        if (l === "") {
                            continue
                        }
                        try {
                            // marker
                            const marker = L.marker([parseFloat(l[0]), parseFloat(l[1])]);

                            // line point
                            pointList.push(new L.LatLng(parseFloat(l[0]), parseFloat(l[1])))

                            let popup = L.popup().setLatLng([parseFloat(l[0]), parseFloat(l[1])]).setContent(
                                '<div id="content">' +
                                '<div id="siteNotice">' +
                                "</div>" +
                                '<h2 style="font-size:150%;" id="firstHeading" class="firstHeading">' + locations[i][0] + '</h1>' +
                                '<div id="bodyContent">' +
                                '<p style="font-size:130%;">' + locations[i][3] + '</p>' +
                                '<a href="' + locations[i][5] + '">' +
                                (locations[i][6] ? "<img src='" + locations[i][6] + "' width='200' height='150'> </a>" : '') +
                                '<p>Link: <a href="' + locations[i][5] + '">' + locations[i][0] +
                                "</p>" +
                                "</div>" +
                                "</div>")

                            marker.bindPopup(popup, {minWidth: 650}).openPopup();

                            markerSet.push(marker);
                            myMarkerClusterGroup.addLayer(marker)
                        } catch (error) {
                            console.log(error)
                        }
                    }
                }
            }
            map.addLayer(myMarkerClusterGroup);
