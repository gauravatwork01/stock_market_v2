import * as trading_view_chart from "https://unpkg.com/lightweight-charts/dist/lightweight-charts.standalone.production.js"




class chart {
    static display_detail(stock_data, ticker = "") {
        if (ticker == "") {
            document.querySelector("div.detail-container").textContent = stock_data[0].data.summary;
        } else {
            for (let ticker_data of stock_data) {
                if (ticker_data.ticker == ticker) {
                    document.querySelector("div.detail-container").textContent = ticker_data.data.summary;
                    break;
                }
            }
        }
    }

    static display_chart(stock_data, selected_ticker, sel_time_dur) {
        // console.log(stock_data);

        const chartOptions = { layout: { textColor: 'black', background: { type: 'solid', color: 'white' } } };
        let graph_cont = document.querySelector('section.graph div.graph-container');
        // console.log(graph_cont.querySelector("div.tv-lightweight-charts"))
        if (graph_cont.querySelector("div.tv-lightweight-charts") != null) {
            graph_cont.querySelector("div.tv-lightweight-charts").remove();
        }
        // .remove();
        //  = "";
        const chart = LightweightCharts.createChart(graph_cont, chartOptions);
        const lineSeries = chart.addLineSeries({ color: '#2962FF' });

        let selected_ticker_data;

        for (let ticker_data of stock_data) {
            if (ticker_data.ticker == selected_ticker) {
                selected_ticker_data = ticker_data;
                break;
            }
        }

        let values = selected_ticker_data.data[sel_time_dur].value;
        let time_stamps = selected_ticker_data.data[sel_time_dur].timeStamp;
        let data = [];
        for (let idx in values) {
            let new_obj = {
                "value": values[idx],
                "time": time_stamps[idx]
            }
            data.push(new_obj);
        }

        lineSeries.setData(data);

        chart.timeScale().fitContent();

        document.querySelector("div.graph-container div#loading").style.visibility = "hidden";
    }
}

// function 

class chart_buttons_cl {

    static stock_data;
    constructor(data) {
        chart_buttons_cl.stock_data = data;
    };

    select_btn(btn) {
        let all_btns = document.querySelectorAll("ul.list-container li > button.btn-selected");
        for (let button of all_btns) {
            button.classList.remove("btn-selected");
            // console.log("hey")
        }

        btn.classList.add("btn-selected");
    }

    add_stock_btn_listener(btn) {

        btn.addEventListener("click", (e) => {
            this.select_btn(btn);
            let ticker = document.querySelector("button.btn-selected");
            ticker = ticker.textContent;

            let time_dur = document.querySelector("div.duration input:checked");
            time_dur = time_dur.value;

            chart.display_chart(chart_buttons_cl.stock_data, ticker, time_dur);
            // let ticker = btn.textContent;
            chart.display_detail(chart_buttons_cl.stock_data, ticker);
        });

    }

    display_stock_list_btns() {
        let stock_data = chart_buttons_cl.stock_data;
        let sec_list_el = document.querySelector("section.list ul");
        let counter = 0;

        for (let obj of stock_data) {
            let new_li = document.createElement("li");
            new_li.innerHTML = `<button>${obj.ticker}</button>
                                <span>$ ${obj.book_value.toFixed(2)}</span>
                                <span>${obj.profit.toFixed(2)}%</span>`;

            sec_list_el.appendChild(new_li);

            let new_btn = new_li.querySelector("button");

            this.add_stock_btn_listener(new_btn);

            counter++;
            if (counter == 1) {
                this.select_btn(new_btn);
            }
        }
        document.querySelector("section.list div#loading").style.visibility = "hidden";
    }

    add_time_dur_btn_listener(rad_inp) {
        rad_inp.addEventListener("change", (e) => {

            let ticker = document.querySelector("button.btn-selected");
            ticker = ticker.textContent;

            let time_dur = document.querySelector("div.duration input:checked");
            time_dur = time_dur.value;
            chart.display_chart(chart_buttons_cl.stock_data, ticker, time_dur);
        })
    }

    display_time_dur_btns() {
        document.querySelector("div.duration").style.visibility = "visible";

        let radio_inputs = document.querySelectorAll("div.duration input[type='radio']");
        for (let radio_inp of radio_inputs) {
            this.add_time_dur_btn_listener(radio_inp);
        }
    }


}





export {
    chart_buttons_cl, chart
};