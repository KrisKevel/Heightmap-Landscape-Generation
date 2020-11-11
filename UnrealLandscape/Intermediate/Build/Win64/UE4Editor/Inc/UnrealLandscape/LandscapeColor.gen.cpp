// Copyright Epic Games, Inc. All Rights Reserved.
/*===========================================================================
	Generated code exported from UnrealHeaderTool.
	DO NOT modify this manually! Edit the corresponding .h files instead!
===========================================================================*/

#include "UObject/GeneratedCppIncludes.h"
#include "UnrealLandscape/LandscapeColor.h"
#ifdef _MSC_VER
#pragma warning (push)
#pragma warning (disable : 4883)
#endif
PRAGMA_DISABLE_DEPRECATION_WARNINGS
void EmptyLinkFunctionForGeneratedCodeLandscapeColor() {}
// Cross Module References
	UNREALLANDSCAPE_API UClass* Z_Construct_UClass_ALandscapeColor_NoRegister();
	UNREALLANDSCAPE_API UClass* Z_Construct_UClass_ALandscapeColor();
	ENGINE_API UClass* Z_Construct_UClass_AActor();
	UPackage* Z_Construct_UPackage__Script_UnrealLandscape();
// End Cross Module References
	void ALandscapeColor::StaticRegisterNativesALandscapeColor()
	{
	}
	UClass* Z_Construct_UClass_ALandscapeColor_NoRegister()
	{
		return ALandscapeColor::StaticClass();
	}
	struct Z_Construct_UClass_ALandscapeColor_Statics
	{
		static UObject* (*const DependentSingletons[])();
#if WITH_METADATA
		static const UE4CodeGen_Private::FMetaDataPairParam Class_MetaDataParams[];
#endif
		static const FCppClassTypeInfoStatic StaticCppClassTypeInfo;
		static const UE4CodeGen_Private::FClassParams ClassParams;
	};
	UObject* (*const Z_Construct_UClass_ALandscapeColor_Statics::DependentSingletons[])() = {
		(UObject* (*)())Z_Construct_UClass_AActor,
		(UObject* (*)())Z_Construct_UPackage__Script_UnrealLandscape,
	};
#if WITH_METADATA
	const UE4CodeGen_Private::FMetaDataPairParam Z_Construct_UClass_ALandscapeColor_Statics::Class_MetaDataParams[] = {
		{ "IncludePath", "LandscapeColor.h" },
		{ "ModuleRelativePath", "LandscapeColor.h" },
	};
#endif
	const FCppClassTypeInfoStatic Z_Construct_UClass_ALandscapeColor_Statics::StaticCppClassTypeInfo = {
		TCppClassTypeTraits<ALandscapeColor>::IsAbstract,
	};
	const UE4CodeGen_Private::FClassParams Z_Construct_UClass_ALandscapeColor_Statics::ClassParams = {
		&ALandscapeColor::StaticClass,
		"Engine",
		&StaticCppClassTypeInfo,
		DependentSingletons,
		nullptr,
		nullptr,
		nullptr,
		UE_ARRAY_COUNT(DependentSingletons),
		0,
		0,
		0,
		0x009000A4u,
		METADATA_PARAMS(Z_Construct_UClass_ALandscapeColor_Statics::Class_MetaDataParams, UE_ARRAY_COUNT(Z_Construct_UClass_ALandscapeColor_Statics::Class_MetaDataParams))
	};
	UClass* Z_Construct_UClass_ALandscapeColor()
	{
		static UClass* OuterClass = nullptr;
		if (!OuterClass)
		{
			UE4CodeGen_Private::ConstructUClass(OuterClass, Z_Construct_UClass_ALandscapeColor_Statics::ClassParams);
		}
		return OuterClass;
	}
	IMPLEMENT_CLASS(ALandscapeColor, 784947247);
	template<> UNREALLANDSCAPE_API UClass* StaticClass<ALandscapeColor>()
	{
		return ALandscapeColor::StaticClass();
	}
	static FCompiledInDefer Z_CompiledInDefer_UClass_ALandscapeColor(Z_Construct_UClass_ALandscapeColor, &ALandscapeColor::StaticClass, TEXT("/Script/UnrealLandscape"), TEXT("ALandscapeColor"), false, nullptr, nullptr, nullptr);
	DEFINE_VTABLE_PTR_HELPER_CTOR(ALandscapeColor);
PRAGMA_ENABLE_DEPRECATION_WARNINGS
#ifdef _MSC_VER
#pragma warning (pop)
#endif
