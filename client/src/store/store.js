import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
    state:{
        status:{},
        parameter:{},
        history:[]
    },
    //Appeler quand on veux recuperer une valeur du store
    getters:{
        status: state => state.status,
        parameter: state => state.parameter,
        history: state => state.history
    },
    //Appeler quand on veux modifier une valeur du store
    mutations:{
        updateStatus(state, payload){
            state.status = {
                ...state.status,
                ...payload
            }
        },
        updateParameter(state, payload){
            state.parameter = {
                ...state.parameter,
                ...payload
            }
        },
        updateHistory(state, payload){
            state.history = payload 
        }
    },
    //Une fonction qui peut etre apeller pour modifier des valeurs
    actions:{
        fetchData(){
            window.axios.get('/status')
            .then(function (response){
                store.commit('updateStatus',response.data)
            })
            // store.commit('updateStatus',{
            //     "light": {
            //       "isForceLight": false,
            //       "isOn": false
            //     },
            //     "serverTime": "Tue, 27 Aug 2019 18:45:02 GMT",
            //     "temperature": {
            //       "temperature": 0
            //     },
            //     "water": {
            //       "currentHumidity": Math.random(),
            //       "isForceWatering": false,
            //       "isWatering": true
            //     }
            // })
            store.commit('updateParameter',{
                'database': {'host': 'littleGarden', 'password': '', 'username': ''},
                'light': {'horaire': {'start': '08:25:00', 'end': '12:42:00'}, 'loop_delay': 10},
                'shutup': {'start': '20:00:00', 'end': '24:00:00'},
                'water': {'after': 5, 'loop_delay': 10, 'open': 10, 'targeted_moister': 2},
                'temperature': {'loop_delay': 10}
            })
        },
        fetchHistory(){
            window.axios.get('/history')
            .then(function (response) {
                console.log(response);
                store.commit('updateHistory',response.data);
            })
        }
    } 
})