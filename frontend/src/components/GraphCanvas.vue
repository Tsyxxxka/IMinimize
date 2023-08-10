<template>
  <div v-loading="loading">
  <!-- <el-tabs type="border-card" style="width: 1450px; height: 2000px;" v-model="method" v-loading="loading">
    <el-tab-pane label="Influence Minimization" name="Min" disabled="method == Max"> -->
      <h2> Seed vertices: {{ sourceNodes }} </h2>
      <h2> Expected influence spread before vertex blocking: {{ originalexp }}</h2>
      <h2> Choose the number of vertices you want to block: </h2>
      <h2> Note: no more than {{maxMuteNumber}}! (i.e., |vertex| - |seed|)</h2>
      <div style="width: 500px; margin-left: 20px; margin-top: 30px; display: inline-block;" >  
        <el-slider v-model="disableNodes"
                   show-tooltip
                   :max="maxMuteNumber">
        </el-slider>
      </div>
      <div style="display: inline-block; margin-left:50px;">
        <el-button type="Primary" @click="mute">Block</el-button>
      </div>
      <div v-if="blocked">
        <h2> ID of vertices we blocked:  {{ disabled }}</h2>
        <h2> Expected influence spread after vertex blocking: {{ afterexp }} </h2>
        <h2> Decline ratio of expected spread: {{ ((originalexp-afterexp)*100/originalexp).toFixed(2) }}%</h2>
      </div>
      <!-- <el-input-number style="margin-left: 20px;" v-model="disableNodes" :min="0" /> -->
      <el-tabs type="border-card" style="margin-top:20px">
        <el-tab-pane label="Show Core Graph">
          <div id="container1"></div>
        </el-tab-pane>
      </el-tabs>
    <!-- </el-tab-pane> -->
  </div>
  <!-- </el-tabs> -->

</template>

<script>
import G6 from '@antv/g6'
import axios from "axios"

export default {
  name: 'GraphCanvas',
  data() {
    return {
      graph : '',
      data : '',
      disableNodes: '',
      disabled: [],
      activatedNodes: '',
      activated: [],
      originalexp: '',
      afterexp: '',
      method: '',
      container: 'container1',
      loading: true,
      sourceNodes: [], // only min
      maxMuteNumber: '',
      // showNodeInfo: false,
      blocked: false
    }
  },
  props: {
    fileName: String,
    minOrmax: String,
  },
  async mounted() {
    this.loading = true
    this.graph = ''
    this.data = ''
    this.disabled = []
    this.method = this.minOrmax
    // this.showNodeInfo = false
    if(this.method == 'Max'){
      this.container = 'container2'
    }
    await this.getData() //get the original data to show the base image
    this.initG6()
    this.disableNodes = 0
    await this.mute()
    this.blocked = false
    this.loading = false
  },
  methods: {
    // async activate() {
    //   this.loading = true
    //   let form = new FormData()
    //   form.append("activate", this.activatedNodes);
    //   form.append("filename", this.fileName);
    //   const res = await axios.post("http://127.0.0.1:8010/activate", form)
    //   this.afterexp = res.data['afterexp']
    //   let nodeNewColor = res.data['nodesColor']
    //   let lenOfData = nodeNewColor.length
    //   this.activated = res.data['seedNodes']
    //   let num = 0
    //   for(; num < lenOfData; num = num + 1) {
    //     this.graph.updateItem(this.graph.findById(nodeNewColor[num]["id"]),{
    //       style: {
    //         fill: '#FF' + nodeNewColor[num]["color"] + nodeNewColor[num]["color"],
    //       }
    //     })
    //   } 
    //   this.loading = false
    // },
    async mute() {
      this.loading = true
      let form = new FormData()
      form.append("mute", this.disableNodes);
      form.append("filename", this.fileName);
      const res = await axios.post("http://127.0.0.1:8010/mute", form)
      this.originalexp = res.data['initialexp']
      if (this.disableNodes != 0) {
        this.afterexp = res.data['afterexp']
      } else {
        this.afterexp = ''
      }
      let nodeNewColor = res.data['nodesColor']
      let lenOfData = nodeNewColor.length
      this.disabled = res.data['muteNodes']
      console.info(res.data)
      let num = 0
      for(; num < lenOfData; num = num + 1) {
        if (nodeNewColor[num]["color"]=='blue'){
          this.graph.updateItem(this.graph.findById(nodeNewColor[num]["id"]),{
            prob: 1,
            style: {
              fill: '#B8C6E5',
              // stroke: '#FF0000'
            }
          })
        } else {
          this.graph.updateItem(this.graph.findById(nodeNewColor[num]["id"]),{
            prob: nodeNewColor[num]["prob"], 
            style: {
              fill: '#FF' + nodeNewColor[num]["color"] + nodeNewColor[num]["color"],
              // stroke: '#FF0000'
            }
          })
        }
      } 
      if (this.disableNodes != 0) {
        this.blocked = true
      } else {
        this.blocked = false
      }
      this.loading = false
    },
    async getData () {
      // for mute to show the original red
      let form = new FormData()
      form.append("filename", this.fileName);
      const res = await axios.post("http://127.0.0.1:8010/hello", form)
      this.sourceNodes = res.data["source"]
      this.data = res.data["data"]
      this.maxMuteNumber = this.data['nodes'].length - this.sourceNodes.length
      // this.showNodeInfo = res.data["showNodeInfo"]
      console.info(this.showNodeInfo)
    },
    initG6() {
        // var showtooltip = this.showNodeInfo == '1'
        const tooltip = new G6.Tooltip({
          offsetX: 10,
          offsetY: 20,
          getContent(e) {
            const outDiv = document.createElement('div');
            outDiv.style.width = '200px';
            outDiv.style.height = '100px'
            var warning = 'no more info'
            if (e.item.getType()=='node'){
              outDiv.innerHTML = `
              <h3>Vertex Info</h3>
                <li>ID: ${e.item.getModel().label || e.item.getModel().id}</li>
                <li>Infected probability: ${e.item.getModel().prob}</li>
                <li>Other info: ${e.item.getModel().nodeInfo || warning}</li>`
            }
            else {
              outDiv.innerHTML = `
              <h3>Edge Info</h3>
                <li>Source: ${e.item.getModel().source}</li>
                <li>Target: ${e.item.getModel().target}</li>
                <li>Activation probability: ${e.item.getModel().prob}</li>`
            }
            return outDiv
          },
          // shouldBegin(){
          //   return showtooltip
          // },
          itemTypes: ['node', 'edge']
        });
        const fisheye = new G6.Fisheye({
          trigger: 'drag',
          d: 1.5,
          r: 200,
          showLabel: true
        });
        const toolbar = new G6.ToolBar();
      this.graph = new G6.Graph({
        // 1.画图挂载容器id
        container: this.container,
        plugins: [tooltip, toolbar, fisheye],
        // 1.1容器宽高
        width: 1200,
        height: 700,
        layout: {
          type: 'force',
          preventOverlap: true,
          nodeSize: 100
        },
        fitview: 'autoZoom',
        defaultNode: {
          size: 40, // 节点大小
          // ...                 // 节点的其他配置
          // 节点样式配置
          style: {
            fill: '#FFFFFF', // 节点填充色
            stroke: '#335A66', // 节点描边色
            lineWidth: 1, // 节点描边粗细
          },
          // 节点上的标签文本配置
          labelCfg: {
            // 节点上的标签文本样式配置
            style: {
              fill: '#000', // 节点标签文字颜色
            },
          },
        },
        // 边在默认状态下的样式配置（style）和其他配置
        defaultEdge: {
          // ...                 // 边的其他配置
          // 边样式配置
          style: {
            opacity: 0.8, // 边透明度
            stroke: 'grey', // 边描边颜色
            endArrow: {
              path: G6.Arrow.triangle(5, 2, 0),
            }
          },
          // 边上的标签文本配置
          // labelCfg: {
          //   autoRotate: true, // 边上的标签文本根据边的方向旋转
          // },
        },

        nodeStateStyles: {
          // 鼠标 hover 上节点，即 hover 状态为 true 时的样式
          //hover: {
          //  fill: 'lightsteelblue',
          //},
          // 鼠标点击节点，即 click 状态为 true 时的样式
          click: {
            stroke: '#335A66',
            lineWidth: 3,
          },
        },
        modes: {
          // default: [
          //   {
          //     type: 'tooltip',
          //     formatText(model) {
          //       return model.xxx;
          //     },
          //     offset: 10,
          //   },
          // ],
          default: ['drag-canvas', 'zoom-canvas', 'drag-node',{
            // type: 'tooltip',
            // formatText: function formatText(model) {
            //   return model.data;
            // },
          }
        ]
        },
      })
      this.graph.data(this.data);
      this.graph.render();
      this.graph.on('node:mouseenter', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 为 true
        this.graph.setItemState(nodeItem, 'hover', true);
      });
      // 监听鼠标离开节点
      this.graph.on('node:mouseleave', (e) => {
        const nodeItem = e.item;
        // 设置目标节点的 hover 状态 false
        this.graph.setItemState(nodeItem, 'hover', false);
      });
      // 监听鼠标点击节点
      this.graph.on('node:click', (e) => {
        // 先将所有当前有 click 状态的节点的 click 状态置为 false
        const clickNodes = this.graph.findAllByState('node', 'click');
        clickNodes.forEach((cn) => {
          this.graph.setItemState(cn, 'click', false);
        });
        const nodeItem = e.item;
        // 设置目标节点的 click 状态 为 true
        this.graph.setItemState(nodeItem, 'click', true);
        
      });
      // 监听鼠标点击节点
      this.graph.on('edge:click', (e) => {
        // 先将所有当前有 click 状态的边的 click 状态置为 false
        const clickEdges = this.graph.findAllByState('edge', 'click');
        clickEdges.forEach((ce) => {
          this.graph.setItemState(ce, 'click', false);
        });
        const edgeItem = e.item;
        // 设置目标边的 click 状态 为 true
        this.graph.setItemState(edgeItem, 'click', true);
      })
   }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style>
h2 {
  color: #335A66;
  font-size: 20px;
  border: none;
  margin-left: 15px;
}
.g6-tooltip {
    border: 1px solid #e2e2e2;
    border-radius: 4px;
    font-size: 12px;
    color: #545454;
    background-color: rgba(255, 255, 255, 0.9);
    padding: 10px 8px;
    box-shadow: rgb(174, 174, 174) 0px 0px 10px;
  }
</style>
