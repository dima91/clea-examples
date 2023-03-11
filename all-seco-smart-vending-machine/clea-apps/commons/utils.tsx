

export const derive_efficiency = (temperature:number, consumption:number, vibration:number, setup:any) : number => {
    let result                  = 100
    let normalized_percentage   = (min:number, max:number, curr:number) => {
        if (curr < min)
            return 0
        if (curr>max)
            return 1
        
        let n_max   = max-min
        let n_curr  = curr-min

        return n_curr/n_max
    }
    let n_t = normalized_percentage(setup.device.minTemperature, setup.device.maxTemperature, temperature)
    let n_c = normalized_percentage(setup.device.minPower, setup.device.maxPower, consumption)
    let n_v = normalized_percentage(setup.device.minVibration, setup.device.maxVibration, vibration)
    
    console.log (`n_% of ${temperature} among ${setup.device.minTemperature} and ${setup.device.maxTemperature} is ${n_t}`)
    console.log (`n_% of ${consumption} among ${setup.device.minPower} and ${setup.device.maxPower} is ${n_c}`)
    console.log (`n_% of ${vibration} among ${setup.device.minVibration} and ${setup.device.maxVibration} is ${n_v}`)

    result  = ((1-((n_t+n_c+n_v)/3))*100).toFixed(2)

    return result
}


export const downsample = (a:any, p:number) => {
    let count   = Math.floor(a.length/100*p)
    let res     = []
    let step	= Math.floor(a.length/count)
    
    // console.log(count)
    // console.log (step)

    let tmp = step
    for (let i in a) {
 			if (tmp == 0)
      	tmp= step/2
      else {
      	tmp--
        res.push(a[i])
      }
    }
    
    return res
}