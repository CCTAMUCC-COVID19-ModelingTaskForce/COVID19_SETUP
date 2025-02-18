import { detectLocale } from '../../i18n/detectLocale'
import { DEFAULT_LOCALE_KEY, LocaleKey, localeKeys } from '../../i18n/i18n'

export interface SettingsState {
  isAutorunEnabled: boolean
  shouldFormatNumbers: boolean
  selectShouldShowPlotLabels: boolean
  isLogScale: boolean
  areResultsMaximized: boolean
  disclaimerVersionAccepted?: number
  disclaimerShouldSuppress: boolean
  localeKey: LocaleKey
  plotYMax: number
  plotXMax: number
  plotYMin: number
  plotXMin: number
}

export const settingsDefaultState: SettingsState = {
  isAutorunEnabled: false,
  shouldFormatNumbers: true,
  selectShouldShowPlotLabels: false,
  isLogScale: true,
  areResultsMaximized: typeof window !== 'undefined' && window?.innerWidth > 2000,
  disclaimerVersionAccepted: undefined,
  disclaimerShouldSuppress: false,
  localeKey: detectLocale({ defaultLanguage: DEFAULT_LOCALE_KEY, availableLocales: localeKeys }),
  plotYMax: 0,
  plotXMax: 0,
  plotYMin: 0,
  plotXMin: 0
}
