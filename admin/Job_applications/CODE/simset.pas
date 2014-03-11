{UNIT Simset implements object oriented set handling using
 doubly linked (two-way) lists. This is an exact emulation of a
 similar facility provided by the programming language SIMULA.

 The representation of two way lists is realized through the public
 classes Head and Link and a common private class called Linkage.
 An object inheriting from Head is considered as a list and its
 members must inherit from Link. Thus objects of different classes
 can enter the same list provided they all are descendants of Link.

 See DISCO documentation and users guide for a detailed description
 and examples of use.

 Ole Nielsen/Mette Olufsen - 1993
 Adapted for Delphi by Ole Nielsen - 1997}


UNIT Simset; {Set handling a la SIMULA in Delphi}

INTERFACE

TYPE
  {*********************************************************************}
  {Class definitions ***************************************************}
  {*********************************************************************}   

  Link = class;   
  Head = class;   

  Linkage = class            {Common class providing basic data structure} 
    function Suc  : Link;    {Pointer to successor in list}
    function Pred : Link;    {Pointer to predecessor in list}
    function Prev : Linkage; {Pointer to predecessor (Link or Head)} 
    constructor init;

    private                  
      Ssuc, Ppred : Linkage; {Actual pointers - must be manipulated indirectly}
      function Me : Linkage; virtual;
  end {Linkage};

  Link = class (Linkage)     {Public class providing the ability to enter list}
    procedure out;                   {Remove calling object from list}
    procedure follow (X : Linkage);  {Insert calling object after X}
    procedure precede (X : Linkage); {Insert calling object before X}
    procedure into (H : Head);       {Insert calling object at end of list}

    private
      function Me : Linkage; override;
  end {Link};

  Head = class (Linkage)     {Public class representing handle to a list}
    procedure clear;                 {Clear entire list} 
    function First    : Link;        {Return pointer to first element}
    function Last     : Link;        {Return pointer to last element}
    function empty    : boolean;     {True if list is empty}
    function cardinal : integer;     {Return number of elements in list}
    
    constructor init;
  end {Head};


IMPLEMENTATION

{*********************************************************************}    
{****** Methods for class Linkage ************************************}
{*********************************************************************}        

constructor Linkage.init;
begin
  Ssuc   := NIL;  Ppred  := NIL;
end {Linkage.init};

function Linkage.Me : Linkage;
begin
  Me := NIL;
end {Linkage.Me};

function Linkage.Suc : Link;
begin
  if Ssuc <> NIL then Suc := Link(Ssuc.Me)
                 else Suc := NIL;
end {Linkage.Suc};

function Linkage.Pred : Link;
begin
  if Ppred <> NIL then Pred := Link (Ppred.Me)
                  else Pred := NIL;
end {Linkage.Pred};

function Linkage.Prev : Linkage;
begin
  Prev := Ppred;
end {Linkage.Prev};


{*********************************************************************}    
{****** Methods for class Link ***************************************}
{*********************************************************************}        

function Link.Me : Linkage;
begin
  Me := self;
end {Link.Me};

procedure Link.out;
begin
  if Ssuc <> NIL then
  begin
    Ssuc.Ppred  := Ppred;
    Ppred.Ssuc  := Ssuc;
    Ssuc        := NIL;
    Ppred       := NIL;
  end;
end {Link.out};

procedure Link.follow (X : Linkage);
begin
  out;
  if (X <> NIL) and (X.Ssuc <> NIL) then
  begin
    Ppred      := X;
    Ssuc       := X.Ssuc;
    X.Ssuc     := Linkage (self);
    Ssuc.Ppred := X.Ssuc;
  end;
end {Link.follow};

procedure Link.precede (X: Linkage);
begin
  out;
  if (X <> NIL) and (X.Ssuc <> NIL) then
  begin
    Ssuc       := X;
    Ppred      := X.Ppred;
    X.Ppred    := Linkage (self);
    Ppred.Ssuc := X.Ppred;
  end;
end {Link.precede};

procedure Link.into (H : Head);
begin
  precede (Linkage (H));
end {Link.into};


{*********************************************************************}    
{****** Methods for class Head ***************************************}
{*********************************************************************}        

constructor Head.init;
begin
  inherited init;
  Ppred  := Linkage (self);
  Ssuc   := Ppred;
end {Head.init};

function Head.First : Link;
begin
  First := Suc;
end {Head.First};

function Head.Last : Link;
begin
  Last := Pred;
end {Head.Last};

function Head.empty : boolean;
begin
  if Ssuc = Linkage (self) then empty := true
                           else empty := false;
end {Head.empty};

function Head.cardinal : integer;
VAR
  i: integer;
  X: Link;
begin
  i := 0;
  X := First;
  while X <> NIL do
  begin
    inc (i);
    X := X.Suc;
  end;
  cardinal := i;
end {Head.cardinal};

procedure Head.clear;
begin
  while First <> NIL do First.out;
end {Head.clear};


{Unit initialisation ******************************************************}

begin {Simset}
end {Unit Simset}.
