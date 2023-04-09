#include "llvm/Analysis/AssumptionCache.h"
#include "llvm/Analysis/InlineCost.h"
#include "llvm/Analysis/ProfileSummaryInfo.h"
#include "llvm/Analysis/TargetLibraryInfo.h"
#include "llvm/Analysis/TargetTransformInfo.h"
#include "llvm/IR/CallingConv.h"
#include "llvm/IR/DataLayout.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/PassManager.h"
#include "llvm/IR/Type.h"
#include "llvm/InitializePasses.h"
#include "llvm/Transforms/IPO.h"
#include "llvm/Support/CommandLine.h"
#include "llvm/Transforms/IPO/Inliner.h"

using namespace llvm;

#define DEBUG_TYPE "inline"

static cl::opt<int>
    MyInlinerCost("my-inliner-cost", cl::init(0),
                  cl::desc("My inliner cost for optimization"));

static cl::opt<int>
    MyInlinerThreshold("my-inliner-threshold", cl::init(225),
                  cl::desc("My inliner threshold for optimization"));


namespace {

class MyInliner : public LegacyInlinerBase {
public:
  static char ID;
  MyInliner() : LegacyInlinerBase(ID), Cost(MyInlinerCost), Threshold(MyInlinerThreshold) {
    errs() << "CALLED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n" << Cost << " " << Threshold << "\n";
  }

  bool runOnSCC(CallGraphSCC &SCC) override {
    return LegacyInlinerBase::runOnSCC(SCC);
  };
  void getAnalysisUsage(AnalysisUsage &AU) const override {
    LegacyInlinerBase::getAnalysisUsage(AU);
  };

  InlineCost getInlineCost(CallBase &CB) override {
    Function *Callee = CB.getCalledFunction();
    if (!Callee || Callee->isDeclaration() || !Callee->hasFnAttribute(Attribute::AttrKind::YourAttribute)) {
      return InlineCost::getNever("Not suitable");
    }
    errs() << "Yes! Got in!" << " " << Cost << " " << Threshold << "\n";
    return InlineCost::get(Cost, Threshold);
  }
private:
  int Cost;
  int Threshold;
};

char MyInliner::ID = 0;

static RegisterPass<MyInliner> X("my-inliner", "My Inliner Pass");
} // namespace