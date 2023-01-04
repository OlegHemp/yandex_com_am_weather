fetch(
    'http://localhost:3001/temp'
).then((res) => res.json()).then( data => setWeather(data));
function setWeather(data){
    document.body.insertAdjacentHTML(
      'afterend',
        `
        <table class="table_dark">
  <tr>
    <th>Местоположение</th>
    <th>Район</th>
    <th>Температура</th>
    <th>Прогноз</th>
    </tr>
    ${setPow(data)}
     </table>
        `
    );
}

function setPow(data) {
    return data.map(
        (location)=>`
        <tr>
            <td>${location["fact_location"]}</td>
            <td>${location["fact_title"]}</td>
            <td>${location["temp_sign"] + location["temp_value"]}</td>
            <td>${location["temp_weather"]}</td>
        </tr>
        `
    ).join(' ');
}
