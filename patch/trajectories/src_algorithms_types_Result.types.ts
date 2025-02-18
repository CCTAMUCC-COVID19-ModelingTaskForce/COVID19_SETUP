import { TimeSeries } from './TimeSeries.types'
import { AgeDistributionDatum } from './Param.types'

export interface InternalCurrentData {
  susceptible: number[]
  exposed: number[][]
  infectious: number[]
  severe: number[]
  critical: number[]
  overflow: number[]
}

export interface InternalCumulativeData {
  recovered: number[]
  hospitalized: number[]
  critical: number[]
  fatality: number[]
}

export interface ExposedCurrentData {
  susceptible: Record<string, number>
  exposed: Record<string, number>
  infectious: Record<string, number>
  severe: Record<string, number>
  critical: Record<string, number>
  overflow: Record<string, number>
  weeklyFatality: Record<string, number>
  infected: Record<string, number>
  dailyNewInfected: Record<string, number>
  weeklyNewInfected: Record<string, number>
}

export interface ExposedCumulativeData {
  recovered: Record<string, number>
  hospitalized: Record<string, number>
  critical: Record<string, number>
  fatality: Record<string, number>
}

// This defines the internal data structure
export interface SimulationTimePoint {
  time: number
  current: InternalCurrentData
  cumulative: InternalCumulativeData
}

// This defines the user-facing data structure
export interface ExportedTimePoint {
  time: number
  current: ExposedCurrentData
  cumulative: ExposedCumulativeData
}

export interface ModelFracs {
  severe: number[]
  critical: number[]
  fatal: number[]
  isolated: number[]
}

export interface ModelRates {
  latency: number
  infection: (t: number) => number
  recovery: number[]
  severe: number[]
  discharge: number[]
  critical: number[]
  stabilize: number[]
  fatality: number[]
  overflowFatality: number[]
}

export interface ModelParams {
  ageDistribution: AgeDistributionDatum[]
  importsPerDay: number[]
  timeDelta: number
  timeDeltaDays: number
  populationServed: number
  numberStochasticRuns: number
  hospitalBeds: number
  icuBeds: number
  frac: ModelFracs
  rate: ModelRates
}

export interface Trajectory {
  middle: ExportedTimePoint[]
  lower: ExportedTimePoint[]
  upper: ExportedTimePoint[]
  percentile: Record<number, ExportedTimePoint[]>
}

export interface TimeSeriesWithRange {
  mean: TimeSeries
  lower: TimeSeries
  upper: TimeSeries
}

export interface PlotDatum {
  time: number
  lines: Record<string, number | undefined>
  areas: Record<string, [number, number] | undefined>
}

export interface AlgorithmResult {
  trajectory: Trajectory
  R0: TimeSeriesWithRange
  plotData: PlotDatum[]
}
