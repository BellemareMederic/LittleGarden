<template>
  <div class="about">
      <input type="date">
      <div class="charts">
        <apexchart class="cards" type=area height=350 :options="chartOptions" :series="series" />
        <apexchart class="cards" type=area height=350 :options="chartOptions" :series="series" />
      </div>
  </div>
</template>
<style lang="scss">
.charts{
  display: flex;
  flex-direction: column;
  .cards{
    flex-grow: 1;
  }
  @include mediaq('medium'){
    flex-direction: row;
    width: 100%;
  }
}
</style>
<script>
export default {
  computed:{
    series() {
      return this.$store.state.history;
    }
  },
  created: function () {
    this.$store.dispatch("fetchHistory");
  },
  data: function(){
    return {
        selection: 'one_year',
        chartOptions: {
          dataLabels: {
            enabled: false
          },

          markers: {
            size: 0,
            style: 'hollow',
          },
          xaxis: {
            type: 'datetime',
            min: new Date('01 Mar 2012').getTime(),
            tickAmount: 6,
          },
          tooltip: {
            x: {
              format: 'dd MMM yyyy'
            }
          },
          fill: {
            type: 'gradient',
            gradient: {
              shadeIntensity: 1,
              opacityFrom: 0.7,
              opacityTo: 0.9,
              stops: [0, 100]
            }
          },
      },
    }
  }
}
</script>