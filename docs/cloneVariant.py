import unreal

def get_asset(path):
	ad = unreal.EditorAssetLibrary.find_asset_data(path)
	o = unreal.AssetRegistryHelpers.get_asset(ad)
	return o
	
def get_primary_asset_id(path):
	return unreal.SystemLibrary.get_primary_asset_id_from_object(unreal.AssetRegistryHelpers.get_asset(unreal.EditorAssetLibrary.find_asset_data(path)))

srcVariant = "NSR-9S"
destVariant = "NSR-9JC"

src_location = "/YetAnotherMechlab/Content/Mechs/Nightstar/"
dest_location = "/SpecialVariants/Objects/Mechs/Nightstar/"

with unreal.ScopedEditorTransaction("Clone Variant Script") as trans:
	unreal.EditorAssetLibrary.duplicate_asset(src_location + srcVariant + "_MDA", dest_location + destVariant + "_MDA")
	unreal.EditorAssetLibrary.duplicate_asset(src_location + srcVariant + "_UnitCard", dest_location + destVariant + "_UnitCard")
	unreal.EditorAssetLibrary.duplicate_asset(src_location + srcVariant + "_Loadout", dest_location + destVariant + "_Loadout")
	destMda = get_asset(dest_location + destVariant + "_MDA")
	destLoadout = get_asset(dest_location + destVariant + "_Loadout")
	destCard = get_asset(dest_location + destVariant + "_UnitCard")
	
	#unreal.log(destMda.mech_data.default_mech)
	#unreal.log(dir(destMda.mech_data.default_mech))
	#unreal.log(destLoadout)
	#unreal.log(dir(destLoadout))
	#unreal.log(get_primary_asset_id(dest_location + destVariant + "_Loadout"))
	destMda.mech_data.set_editor_property("variant_name", destVariant);
	destMda.mech_data.default_mech.set_editor_property("id", get_primary_asset_id(dest_location + destVariant + "_Loadout"))

	destLoadout.mech_loadout.mech_data_asset_id.set_editor_property("id", get_primary_asset_id(dest_location + destVariant + "_MDA"))
	destCard.unit_card.set_editor_property("mech_loadout_template", destMda.mech_data.default_mech)
	
	#unreal.log(dir(o.mech_data))
	#unreal.log(o.mech_data.variant_name)
	#unreal.log(o.mech_data.default_mech)
	#unreal.log(get_primary_asset_id(asset_location + srcVariant + "_Loadout"))
