## Patch files
This directory contains files that replace files in `neherlab/covid19_scenarios`.
They should work with version 1.8.0 (commit: `c6e611bcc87f01a8160530cf74f4e8e3ea1f0b0f`).

#### Patch `plotControls`: control plot axes 

Adds spinboxes to select min and max values for x and y axes.

	# Backup originals
	cp ../../src/state/settings/settings.actions.ts \
		plotControls/src_state_settings_settings.actions.ts.orig
	cp ../../src/state/settings/settings.reducer.ts \
		plotControls/src_state_settings_settings.reducer.ts.orig
	cp ../../src/state/settings/settings.sagas.ts \
		plotControls/src_state_settings_settings.sagas.ts.orig
	cp ../../src/state/settings/settings.selectors.ts \
		plotControls/src_state_settings_settings.selectors.ts.orig
	cp ../../src/state/settings/settings.state.ts \
		plotControls/src_state_settings_settings.state.ts.orig
	cp ../../src/components/Main/Controls/SettingsControls.tsx \
		plotControls/src_components_Main_Controls_SettingsControls.tsx.orig
	cp ../../src/components/Main/Results/DeterministicLinePlot.tsx \
		plotControls/src_components_Main_Results_DeterministicLinePlot.tsx.orig

	# Replace with patched
	cp plotControls/src_state_settings_settings.actions.ts \ 
		../../src/state/settings/settings.actions.ts
	cp plotControls/src_state_settings_settings.reducer.ts \
		../../src/state/settings/settings.reducer.ts
	cp plotControls/src_state_settings_settings.sagas.ts \
		../../src/state/settings/settings.sagas.ts
	cp plotControls/src_state_settings_settings.selectors.ts \
		../../src/state/settings/settings.selectors.ts
	cp plotControls/src_state_settings_settings.state.ts \
		../../src/state/settings/settings.state.ts
	cp plotControls/src_components_Form_KrellSpinBox.tsx \
		../../src/components/Form/KrellSpinBox.tsx
	cp plotControls/src_components_Main_Controls_SettingsControls.tsx \
		../../src/components/Main/Controls/SettingsControls.tsx
	cp plotControls/src_components_Main_Results_DeterministicLinePlot.tsx \
		../../src/components/Main/Results/DeterministicLinePlot.tsx


