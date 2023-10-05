var map = L.map('map').setView([20, 0], 2);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let visitedCountries = new Set();

fetch('https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json')
    .then(response => response.json())
    .then(data => {
        L.geoJSON(data, {
            style: {
                color: '#000',
                weight: 1,
                fillOpacity: 0.3
            },
            onEachFeature: (feature, layer) => {
                layer.on('click', function () {
                    const countryName = feature.properties.name;

                    if (layer.hasClass('visited')) {
                        layer.removeClass('visited');
                        visitedCountries.delete(countryName);
                    } else {
                        layer.addClass('visited');
                        visitedCountries.add(countryName);
                    }

                    updateCounterAndList();
                });
            }
        }).addTo(map);
    });

L.Path.include({
    hasClass: function (className) {
        return this._path.className && this._path.className.baseVal.indexOf(className) !== -1;
    },
    addClass: function (className) {
        if (this._path.className && !this.hasClass(className)) {
            this._path.className.baseVal = this._path.className.baseVal + ' ' + className;
        }
    },
    removeClass: function (className) {
        if (this.hasClass(className)) {
            this._path.className.baseVal = this._path.className.baseVal.replace(new RegExp('(\\s|^)' + className + '(\\s|$)', 'g'), '$2');
        }
    }
});

function updateCounterAndList() {
    const counterEl = document.getElementById('counter');
    counterEl.textContent = visitedCountries.size;
}

document.getElementById('downloadBtn').addEventListener('click', function () {
    const blob = new Blob([Array.from(visitedCountries).join('\n')], { type: 'text/plain' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'visited_countries.txt';
    a.click();
});
