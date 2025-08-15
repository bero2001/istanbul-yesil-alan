const istanbulBounds = [[27.0, 40.7], [30.7, 41.5]];

const map = new maplibregl.Map({
  container: 'map',
  style: 'https://api.maptiler.com/maps/basic/style.json?key=7HURHNYJKglNoxfFEHYp',
  center: [28.80303, 41.16259],
  minZoom: 9,
  maxZoom: 16,
  maxBounds: istanbulBounds
});

map.on('load', async () => {
  const ilceData = await fetch('ilce_geojson.json').then(r => r.json());
  const yesilData = await fetch('yesil_alanlar.geojson').then(r => r.json());

  ilceData.features.forEach(f => {
    f.properties.ilceAd = f.properties.address?.town || f.properties.Town || 'Bilinmeyen';
    f.properties.kisi_basi_m2 = 0;
    f.properties.yesilalan_m2 = 0;
  });

  map.addSource('ilceler', { type: 'geojson', data: ilceData });

  map.addLayer({
    id: 'ilce-fill',
    type: 'fill',
    source: 'ilceler',
    paint: {
      'fill-color': [
        'interpolate', ['linear'], ['get', 'kisi_basi_m2'],
        0, '#cccccc', 2, '#ffff00', 5, '#90ee90', 10, '#006400'
      ],
      'fill-opacity': 0.6
    }
  });

  map.addLayer({
    id: 'ilce-outline',
    type: 'line',
    source: 'ilceler',
    paint: { 'line-color': '#333', 'line-width': 1.5 }
  });

  map.on('click', 'ilce-fill', async (e) => {
    const clickedIlceAd = e.features[0].properties.ilceAd;
    const fullIlce = ilceData.features.find(f => f.properties.ilceAd === clickedIlceAd);

    document.getElementById('loading').style.display = 'block';

    let toplamYesilAlan = 0, kisiBasi = 0;
    let parcaliYesilAlanlar = [];

    try {
      const res = await fetch(`http://127.0.0.1:8000/ilceler/${encodeURIComponent(clickedIlceAd)}`);
      const data = await res.json();
      toplamYesilAlan = data.yesil_alan_m2;
      kisiBasi = data.kisi_basi_m2;

      const yesilRes = await fetch(`http://127.0.0.1:8000/yesil_alanlar/${encodeURIComponent(clickedIlceAd)}`);
      const yesilJson = await yesilRes.json();

      parcaliYesilAlanlar = yesilData.features
        .map(p => turf.intersect(p, fullIlce))
        .filter(Boolean);

    } catch (e) {
      alert("Veri alınamadı");
    } finally {
      document.getElementById('loading').style.display = 'none';
    }

    ilceData.features.forEach(f => {
      f.properties.kisi_basi_m2 = 0;
      f.properties.yesilalan_m2 = 0;
    });
    fullIlce.properties.kisi_basi_m2 = kisiBasi;
    fullIlce.properties.yesilalan_m2 = toplamYesilAlan;
    map.getSource('ilceler').setData(ilceData);

    if (map.getSource('yesil-alanlar')) {
      if (map.getLayer('yesil-alan-fill')) map.removeLayer('yesil-alan-fill');
      if (map.getLayer('yesil-alan-outline')) map.removeLayer('yesil-alan-outline');
      map.removeSource('yesil-alanlar');
    }

    map.addSource('yesil-alanlar', {
      type: 'geojson',
      data: { type: 'FeatureCollection', features: parcaliYesilAlanlar }
    });

    map.addLayer({
      id: 'yesil-alan-fill',
      type: 'fill',
      source: 'yesil-alanlar',
      paint: { 'fill-color': '#2ecc71', 'fill-opacity': 0 }
    });

    map.addLayer({
      id: 'yesil-alan-outline',
      type: 'line',
      source: 'yesil-alanlar',
      paint: { 'line-color': '#27ae60', 'line-width': 1 }
    });

    let opacity = 0;
    const interval = setInterval(() => {
      opacity += 0.05;
      if (opacity >= 0.4) {
        map.setPaintProperty('yesil-alan-fill', 'fill-opacity', 0.4);
        clearInterval(interval);
      } else {
        map.setPaintProperty('yesil-alan-fill', 'fill-opacity', opacity);
      }
    }, 30);

    new maplibregl.Popup()
      .setLngLat(e.lngLat)
      .setHTML(`<strong>${clickedIlceAd}</strong><br>Toplam Yeşil Alan: ${toplamYesilAlan.toFixed(2)} m²<br>Kişi Başı Yeşil Alan: ${kisiBasi.toFixed(2)} m²`)
      .addTo(map);

    const ctx = document.getElementById('barChart').getContext('2d');
if (window.barChartInstance) window.barChartInstance.destroy();

window.barChartInstance = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: ['Toplam Alan', 'Kişi Başı Alan'],
    datasets: [
      {
        label: 'Toplam Yeşil Alan',
        data: [toplamYesilAlan, null],
        backgroundColor: '#2ecc71',
        yAxisID: 'y1'
      },
      {
        label: 'Kişi Başı Alan',
        data: [null, kisiBasi],
        backgroundColor: '#3498db',
        yAxisID: 'y2'
      }
    ]
  },
  options: {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    title: {
      display: true,
      text: `${clickedIlceAd}`,
      font: {
        size: 16
      }
    },
    legend: {
      display: false
    }
  },
  scales: {
    y1: {
      beginAtZero: true,
      position: 'left',
      title: {
        display: true,
        text: 'Toplam Yeşil Alan (m²)',
        font: { size: 10 }
      },
      ticks: {
        font: { size: 10 }
      }
    },
    y2: {
      beginAtZero: true,
      position: 'right',
      grid: { drawOnChartArea: false },
      title: {
        display: true,
        text: 'Kişi Başı Alan (m²)',
        font: { size: 10 }
      },
      ticks: {
        font: { size: 10 }
      }
    },
    x: {
      ticks: {
        font: { size: 11 }
      }
    }
  }
}

});



    document.getElementById("barChartContainer").style.display = "block";
  });
});


// JS dosyası
