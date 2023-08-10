<template>
  <!-- <el-tabs type="border-card" style="width: 1000px; height: 700px; border-radius: 30px" >
    <el-tab-pane label="Choose Settings for UI" style="margin-top: 50px;"> -->
      <el-form :model="form" style="margin-left: 230px;" class="elformclass">
        <el-form-item label="Show Vertex Label">
          <el-radio-group v-model="form.shownodeInfo" style="margin-left: 140px">
            <el-radio label="Yes"></el-radio>
            <el-radio label="No"></el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Show Edge Label">
          <el-radio-group v-model="form.showedgeInfo" style="margin-left: 150px">
            <el-radio label="Yes"></el-radio>
            <el-radio label="No"></el-radio>
          </el-radio-group>
        </el-form-item>

        <!-- <el-tooltip content="Set this if you want to download the result bag of this run." placement="top">
          <el-form-item label="Tag for this run (optional)">
            <el-input 
              :rows="5" 
              clearable 
              maxlength="30"
              show-word-limit
              type="textarea" 
              v-model="form.Tag" 
              style="width: 250px;"
              placeholder="Please enter TAG for this run. It will be used to name your result package."
              >
            </el-input>
          </el-form-item>
        </el-tooltip> -->
      </el-form>
    <!-- </el-tab-pane>
  </el-tabs> -->
</template>

<script>
export default {
  name: 'Go',
  data() {
    return {
      form: {
        // Tag: '',
        shownodeInfo: '',
        showedgeInfo: '',
      }
    }
  },
  watch: {
    form:{
      handler() {
        this.showSettings()
      },
      deep: true
    }
  },
  methods: {
    showSettings () {
      this.$emit("getShowSettings", this.form)
    }
  }
}
</script>

<style>
.elformclass .el-form-item__label {
  font-size: 20px;
  color: #335A66;
}
</style>
<style scoped>
.el-form-item {
  height: 50px;
}

.el-radio /deep/ .el-radio__label {
  font-size: 20px;
  color: #335A66;
}
</style>