#!/usr/bin/env node

const UVCControl = require('../index')

const ops = new Object()

ops.vid = 1133
ops.pid = 2120
ops.deviceAddress = 12



const cam = new UVCControl(ops)
console.log(cam.supportedControls)
