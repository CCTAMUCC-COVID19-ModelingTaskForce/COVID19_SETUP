## Patch files
This directory contains files that replace files in `neherlab/covid19_scenarios`.
They should work with version 1.8.0 (commit: `c6e611bcc87f01a8160530cf74f4e8e3ea1f0b0f`).

#### Patch `plotControls`: control plot axes 

Adds spinboxes to select min and max values for x and y axes.

	# Backup originals
	cp ../src/state/settings/actions.ts \
		plotControls/src_state_settings_actions.ts.orig
	cp ../src/state/settings/reducer.ts \
		plotControls/src_state_settings_reducer.ts.orig
	cp ../src/state/settings/sagas.ts \
		plotControls/src_state_settings_sagas.ts.orig
	cp ../src/state/settings/selectors.ts \
		plotControls/src_state_settings_selectors.ts.orig
	cp ../src/state/settings/state.ts \
		plotControls/src_state_settings_state.ts.orig
	cp ../src/components/Form/KrellSpinBox.tsx \
		plotControls/src_components_Form_KrellSpinBox.tsx.orig
	cp ../src/components/Main/Controls/SettingsControls.tsx \
		plotControls/src_components_Main_Controls_SettingsControls.tsx.orig
	cp ../src/components/Main/Results/DeterministicLinePlot.tsx \
		plotControls/src_components_Main_Results_DeterministicLinePlot.tsx.orig

	# Replace with patched
	cp plotControls/src_state_settings_actions.ts \ 
		../src/state/settings/actions.ts
	cp plotControls/src_state_settings_reducer.ts \
		../src/state/settings/reducer.ts
	cp plotControls/src_state_settings_sagas.ts \
		../src/state/settings/sagas.ts
	cp plotControls/src_state_settings_selectors.ts \
		../src/state/settings/selectors.ts
	cp plotControls/src_state_settings_state.ts \
		../src/state/settings/state.ts
	cp plotControls/src_components_Form_KrellSpinBox.tsx \
		../src/components/Form/KrellSpinBox.tsx
	cp plotControls/src_components_Main_Controls_SettingsControls.tsx \
		../src/components/Main/Controls/SettingsControls.tsx
	cp plotControls/src_components_Main_Results_DeterministicLinePlot.tsx \
		../src/components/Main/Results/DeterministicLinePlot.tsx


