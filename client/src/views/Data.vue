<template>
  <div class="about">
    <div id="chart">
      <!-- <div class="toolbar">
        <button @click="updateData('one_month')" id="one_month" :class="{active: selection==='one_month'}">1M</button>
        <button @click="updateData('six_months')" id="six_months" :class="{active: selection==='six_months'}">6M</button>
        <button @click="updateData('one_year')" id="one_year" :class="{active: selection==='one_year'}">1Y</button>
        <button @click="updateData('ytd')" id="ytd" :class="{active: selection==='ytd'}">YTD</button>
        <button @click="updateData('all')" id="all" :class="{active: selection==='all'}">ALL</button>
      </div> -->
      <input type="date">
      <apexchart type=area height=350 :options="chartOptions" :series="series" />
    </div>
  </div>
</template>
<script>
export default {
  computed:{
    series() {
      return [{
        data: this.$store.getters.history
      }]
    }
  },
  created: function () {
    this.$store.dispatch("fetchHistory");
  },
  data: function(){
    return {
        selection: 'one_year',
        chartOptions: {
        //   annotations: {
        //     yaxis: [{
        //       y: 30,
        //       borderColor: '#999',
        //       label: {
        //         show: true,
        //         text: 'Support',
        //         style: {
        //           color: "#fff",
        //           background: '#00E396'
        //         }
        //       }
        //     }],
        //     xaxis: [{
        //       x: new Date('14 Nov 2012').getTime(),
        //       borderColor: '#999',
        //       yAxisIndex: 0,
        //       label: {
        //         show: true,
        //         text: 'Rally',
        //         style: {
        //           color: "#fff",
        //           background: '#775DD0'
        //         }
        //       }
        //     }]
        //   },
        //   dataLabels: {
        //     enabled: false
        //   },

        //   markers: {
        //     size: 0,
        //     style: 'hollow',
        //   },
        //   xaxis: {
        //     type: 'datetime',
        //     min: new Date('01 Mar 2012').getTime(),
        //     tickAmount: 6,
        //   },
        //   tooltip: {
        //     x: {
        //       format: 'dd MMM yyyy'
        //     }
        //   },
          // fill: {
          //   type: 'gradient',
          //   gradient: {
          //     shadeIntensity: 1,
          //     opacityFrom: 0.7,
          //     opacityTo: 0.9,
          //     stops: [0, 100]
          //   }
          // },
      },
    }
  }
}
</script>