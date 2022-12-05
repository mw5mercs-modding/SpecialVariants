# Creating Variants for YAML

## Disclaimer

This guide describes how to create new 'Mech variants for existing 'Mechs. It does not go into detail about creating new 'Mech or weapon models.

## Overview

In general a variant requires three assets:

* a UnitCard contains things like the introduction date or the faction rarities.
* a MechData Asset (MDA) contains the technical values like armor or the weapon hardpoints and equipment slots.
* a Loadout is what it's name suggests: the installed weapons and equipment along with the default weapon groups.

For simplicity and easy scripting these assets should follow a consistent naming scheme as follows:

* `VARIANT_NAME_UnitCard`
* `VARIANT_NAME_MDA`
* `VARIANT_NAME_Loadout`

## Preparation

* Install the editor
* Disable Hot reload
* Get sources for YAML and YAWC for simplicity
* Optionally: get sources for SpecialVariants and Harjel

## Step 1: Choose a Variant

The first step is the simplest: choose the variant you want to create. Ideally not one already contained in YAML, it's mech mod, Mace's lore-accurate variants mod or even trueg's SpecialVariants. Good sources for variants and their loadouts are [the Sarna Battletech wiki](https://www.sarna.net/wiki/Main_Page), [Roguetech's excellent mech documentation](https://roguetech.fandom.com/wiki/Mechs) and [MegaMekLab](http://megameklab.sourceforge.net/).

See the list of [existing YAML variants](yaml-variants.md) to make sure you do not duplicate work.

## Step 2: Decide the best mod for your variant

While you can of course always choose to release your variant in a separate mod, it might be good to collaborate instead and try to get your variant into one of the existing mods. A good rule of thumb might be this:

* your variant uses vanilla or YAW weapons only -> YAML
* your variant uses Clan weapons or equipment from YAWC -> Yet Another Clan Mech
* your variant uses equipment from "The Equipment Collection Formerly Known As Harjel" -> SpecialVariants

## Step 3: Clone an existing variant's assets

If the mod already contains a variant of the chassis of your choice then you can continue with the clone script below. Otherwise copy the 3 required files from the YAML sources into the mod's `Content` folder. (Never directly use assets copied with the file manager, always clone them, otherwise the internal id will not change and you end up with a conflict!)

Use the [`cloneVariant.py`](cloneVariant.py) script to clone an existing variant into the mod of your choosing. To that end modify the source and destination variant and paths accordingly (right-click an asset in the editor and select "copy reference" if you have trouble figuring out the paths). Python scripts can be executed from the editor via `File`->`Python`.

The script will create the necessary assets and set the cross-references accordingly.

Once cloned you can delete the 3 assets you copied via the file manager (never delete assets in the editor, it will take forever, instead close the editor, delete them in the file manager and restart the editor).

## Step 4: Modify the UnitCard

The important values of the unit card are:

* Intro Usage (`Unit.Usage.Market` or `Unit.Usage.Unique`) defines if it will spawn on markets / as enemy. Unique units (Heroes) have different spawn rules.
* The introduction date (only the year is of relevance)
* The faction rarities define which enemy factions will be able to field the variant in missions.
* Attributes (`Unit.Usage.InstantAction`) (at the end of UnitCard) defines if the mech is visible in Instant Action lists. If you want to hide the variant from IS, just delete the tag. It will still spawn as enemy / on markets as defined above.

## Step 5: Modify the MDA

First set the basics:

* Change the description (Sarna and the Roguetech wiki are your friends again)
* Set the number of salvage shares (if you think they should be different)

Then comes the only part that can sometimes get tricky: the weapon hardpoints.

## Step 6: Create the Loadout

Right-click your loadout asset in the editor and select "Bulk Export". This will create a json representation of the loadout in the same folder as the asset. We will overwrite this later.

Now comes the fun part. Package the mod and run it in the game proper. Navigate to "Single Player->Instant Action", select your variant, build the loadout to your liking, and finally save it.

This will actually save the loadout in a json file that we can use to import the loadout into the editor.

Open the instant action save file from `<APPDATA>/Local/MW5Mercs/Saved/SavedLoadouts/InstantAction.json` - ideally in an editor like Notepad++. Find your loadout and copy the content of `mechLoadout` into the previously exported loadout json file (check the original file to make sure you have the correct element.

Now set the `customName`value to an empty string (we do no need it) and save the file.

Back in the editor right-click the loadout asset again and re-import.

## Step 7: Quirks