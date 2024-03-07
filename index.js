
// document.querySelector("h3").style.backgroundColor = "orange";
// import { chart_buttons_cl, display_stock_list, display_chart, display_detail, display_time_dur_btns } from "./display.js";
import { chart_buttons_cl, chart } from "./display.js";


async function fetch_stock_data() {

    let stock_data_response = await fetch("https://stocks3.onrender.com/api/stocks/getstocksdata");
    let stock_data_json = await stock_data_response.json();
    stock_data_json = stock_data_json.stocksData[0];

    let stock_summary_resp = await fetch("https://stocks3.onrender.com/api/stocks/getstocksprofiledata");
    let stock_summary_json = await stock_summary_resp.json();
    stock_summary_json = stock_summary_json.stocksProfileData[0];

    let stock_other_resp = await fetch("https://stocks3.onrender.com/api/stocks/getstockstatsdata");
    let stock_other_json = await stock_other_resp.json();
    stock_other_json = stock_other_json.stocksStatsData[0];

    return [stock_data_json, stock_summary_json, stock_other_json];
}

fetch_stock_data().then(([stock_data, stock_summary, stock_other]) => {
    let compl_stock_data = [];

    let keys_arr = Object.keys(stock_data);
    keys_arr.splice(0, 1);

    for (let key of keys_arr) {
        let new_obj = {
            "ticker": key,
            "book_value": stock_other[key].bookValue,
            "profit": stock_other[key].profit,
            "data": stock_data[key]
        }
        new_obj.data.summary = stock_summary[key].summary;
        compl_stock_data.push(new_obj);

    }

    let chart_obj = new chart_buttons_cl(compl_stock_data);
    chart_obj.display_stock_list_btns();
    chart_obj.display_time_dur_btns();

    let ticker = document.querySelector("button.btn-selected");
    ticker = ticker.textContent;

    let time_dur = document.querySelector("div.duration input:checked");
    time_dur = time_dur.value;


    chart.display_chart(compl_stock_data, ticker, time_dur)
    chart.display_detail(compl_stock_data, ticker);

});





