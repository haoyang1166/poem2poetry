<template>
  <el-container>
    <el-header>
      <el-row>
        <el-col :span="24">
          <div>
            <h3>唐代诗人社交网络分析</h3>
          </div>
        </el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-main>
        <el-row>
          <el-col
            :span="24"
            class="textFontSize"
          >
            <el-tabs @tab-click="handleClick">
              <el-tab-pane
                label="全唐"
                name="full"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="1"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="drawEcharts()"
                    >查看社交网络图</el-button>
                  </el-col>
                </el-row>
                <div
                  id="echart"
                  class="echart-div1"
                ></div>
              </el-tab-pane>
              <el-tab-pane
                label="早唐"
                name="early"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="1"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="drawEcharts2()"
                    >查看社交网络图</el-button>
                  </el-col>
                </el-row>
                <div
                  id="echart2"
                  class="echart-div2"
                ></div>
              </el-tab-pane>
              <el-tab-pane
                label="中唐"
                name="middle"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="1"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="drawEcharts3()"
                    >查看社交网络图</el-button>
                  </el-col>
                </el-row>
                <div
                  id="echart3"
                  class="echart-div3"
                ></div>
              </el-tab-pane>
              <el-tab-pane
                label="盛唐"
                name="high"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="1"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="drawEcharts4()"
                    >查看社交网络图</el-button>
                  </el-col>
                </el-row>
                <div
                  id="echart4"
                  class="echart-div4"
                ></div>
              </el-tab-pane>
              <el-tab-pane
                label="晚唐"
                name="late"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="1"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="drawEcharts5()"
                    >查看社交网络图</el-button>
                  </el-col>
                </el-row>
                <div
                  id="echart5"
                  class="echart-div5"
                ></div>
              </el-tab-pane>
              <el-tab-pane
                label="自定义诗人"
                name="custom"
              >
                <el-row :gutter="20">
                  <el-col
                    :span="3"
                    class="textFontSize"
                  >
                    <el-button
                      type="primary"
                      @click="getCustomPoemsData()"
                    >查看社交网络图</el-button>
                  </el-col>
                  <el-col :span="10">
                    <el-select
                      v-model="poetList"
                      multiple
                      filterable
                      @change="selectPoetChange"
                    >
                      <el-option
                        v-for="(item,index) in poetOptions"
                        :key="index"
                        :label="item.label"
                        :value="item.value"
                      />
                    </el-select>
                  </el-col>
                </el-row>
                <div
                  id="echart6"
                  class="echart-div6"
                ></div>
              </el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </el-main>
    </el-container>
  </el-container>
</template>
<script>

export default {
  data() {
    return {
      data: [],
      timeParams: {},
      custom: false,
      poetOptions: [],
      poetList: [],
      myChart: ''
    }
  },
  created() {
  },
  methods: {
    handleClick(tab, event) {
      var data = {
        data: tab.name
      }
      if (tab.name === 'custom') {
        this.custom = true
        this.getSelectOptions()
      } else {
        this.custom = false
        this.timeParams = data
        this.getPoemsData()
      }
      console.log(this.timeParams)
    },
    drawEcharts() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawEcharts2() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart2'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawEcharts3() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart3'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawEcharts4() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart4'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawEcharts5() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart5'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      myChart.setOption(option)
    },
    drawEcharts6() {
      var datas = []
      for (const v of this.data.data) {
        const temp = { name: v.name, itemStyle: { color: '#000000' } }
        datas.push(temp)
      }
      let myChart = this.$echarts.init(document.getElementById('echart6'))
      var that = this
      let option = {
        title: {
          text: '',
          top: '80%',
          left: '50%'
        },
        tooltip: {},
        animation: false,
        series: [
          {
            name: '唐朝诗人社交网络',
            type: 'graph',
            layout: 'force',
            draggable: true,

            symbolSize: 28,
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 6],
            lineStyle: {
              normal: {
                curveness: 0.1,
                color: 'rgb(50, 50, 50)'
              }
            },
            data: datas,
            links: that.data.link,
            roam: true,
            label: {
              normal: {
                show: true,
                position: 'inside',
                formatter: '{b}',
                textStyle: {
                  fontSize: 10
                }
              }
            },
            force: {
              repulsion: 100
            }
          }
        ]
      }
      console.log('option')
      console.log(option)
      myChart.setOption(option)
    },
    getPoemsData() {
      this.$axios(
        {
          method: 'GET',
          url: 'http://localhost:5000/data',
          params: this.timeParams,
          dataType: 'json',
          contentType: 'multipart/form-data'
        }
      ).then((response) => {
        console.log(response)
        this.data = response.data
        console.log(this.data)
      }).catch((response) => {
        console.log('error')
      })
    },
    getCustomPoemsData() {
      var dataString = ''
      for (const v of this.poetList) {
        dataString = dataString + v + ','
      }
      var data = {
        data: dataString
      }
      console.log(data)
      this.$axios(
        {
          method: 'GET',
          url: 'http://localhost:5000/custom',
          // params: this.poetCustom,
          params: data,
          // traditional: true,
          dataType: 'json'
          // contentType: 'multipart/form-data'
        }
      ).then((response) => {
        console.log(response)
        this.data = response.data
        this.drawEcharts6()
      }).catch((response) => {
        console.log('error')
      })
    },
    getSelectOptions() {
      this.$axios(
        {
          method: 'GET',
          url: 'http://localhost:5000/select',
          // data: data,
          dataType: 'json'
        }
      ).then((response) => {
        this.poetOptions = []
        // console.log(response)
        for (const v of response.data.res) {
          var temp = {}
          temp.label = v
          temp.value = v
          this.poetOptions.push(temp)
        }
        // console.log(this.poetOptions)
      }).catch((response) => {
        console.log('error')
      })
    },
    selectPoetChange(val) {
      // this.getCustomPoemsData()
    }
  }
}
</script>
<style lang='scss' scoped>
.el-header {
  background-color: #2b324e;
  color: #fff;
}

.el-aside {
  background-color: #2b324e;
  color: #fff;
}

.el-main {
  background-color: #fff;
  color: #000000;
  .upload {
    height: 100px;
  }
}
.el-table,
.el-table__expanded-cell {
  background-color: transparent;
}
.el-table th,
.el-table tr {
  background-color: transparent;
}
.el-button {
  background-color: #2b324e;
  color: #fff;
}
.echart-div1 {
  height: 800px;
  width: 80%;
}
.echart-div2 {
  height: 500px;
  width: 80%;
}
.echart-div3 {
  height: 500px;
  width: 80%;
}
.echart-div4 {
  height: 500px;
  width: 80%;
}
.echart-div5 {
  height: 500px;
  width: 80%;
}
.echart-div6 {
  height: 800px;
  width: 80%;
}
</style>
