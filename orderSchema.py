from datetime import datetime
from typing import Any, List, Optional
from bson import ObjectId
from typing_extensions import TypedDict


# ── Reusable sub-schemas ──────────────────────────────────────────────────────

class TaxSetupUSA(TypedDict, total=False):
    stateTax: float
    countyTax: float
    localTax: float


class TaxSetupCANADA(TypedDict, total=False):
    PST: float
    GST: float
    HST: float


class TaxSetup(TypedDict, total=False):
    USA: TaxSetupUSA
    CANADA: TaxSetupCANADA


class TaxEntry(TypedDict, total=False):
    taxRef: ObjectId
    taxName: str
    taxRate: float
    isTaxInclusive: bool
    taxAmount: float
    refundedTaxAmount: float
    taxType: str  # enum: TAX_TYPE


class IngredientUsed(TypedDict, total=False):
    ingredientRef: ObjectId
    isArchived: bool
    quantity: float
    costPrice: float


class TransferRefund(TypedDict, total=False):
    transferId: str
    amount: float
    refundApplicationFee: float


class Transfer(TypedDict, total=False):
    transferId: str
    vendorId: ObjectId
    vendorType: str
    amount: float
    account: str
    feePercentage: float
    shareAmount: float
    applicationFee: float
    vatAmount: float
    vatCommissionType: str
    vatRateOnCommission: float
    revenueShare: float
    refundedAmount: float
    refunds: List[TransferRefund]
    softwareFeePOSTotal: float
    softwareFeeRevenueShareTotal: float
    hardwareFeeTotal: float
    mscFeeTotal: float
    platformFeeTotal: float


class FeeBreakdown(TypedDict, total=False):
    variable: Optional[float]
    fix: Optional[float]


class AdyenTransaction(TypedDict, total=False):
    isCloudPayment: bool
    tid: str
    fee: float
    storeId: str
    paymentPspReference: str
    fundingSource: str
    issuerCountry: str
    cardIssuingBank: str
    capturePspReference: str
    sessionId: str
    payByLinkId: str
    verified: bool
    saleId: str
    poiId: str
    commissionRoundOfAmount: float
    serviceId: str
    tenderReference: str
    adyenInterchangeFee: dict
    adyenFee: FeeBreakdown
    feeBalanceAccountRef: Optional[ObjectId]
    unconfirmedBatchCount: int
    isAuthChargeCancelled: bool
    cardTokenValue: Optional[str]


class TidyPay(TypedDict, total=False):
    accountId: str
    transactionId: str
    token: str


class CardData(TypedDict, total=False):
    cardType: str
    lastFourDigit: str


class PaidItem(TypedDict, total=False):
    itemId: ObjectId
    quantity: float


class TransactionTier(TypedDict, total=False):
    _id: ObjectId
    lowerBound: float
    upperBound: float
    commissionBasis: str
    vatAmount: float
    vatCommissionType: str
    vatRateOnCommission: float
    totalCommission: float
    commissionPercentage: float
    amountAllocated: float
    tierRef: Optional[ObjectId]


class Transaction(TypedDict, total=False):
    paymentType: str          # enum: TRANSACTION_PAYMENT_TYPE, default "CARD"
    paymentMode: Optional[str]
    paymentGateway: str
    stripePaymentIntentId: str
    stripePaymentMethodId: str
    stripeSourceTransactionId: str
    stripeChargeId: str
    stripeReceiptUrl: str
    status: str               # enum: TRANSACTION_PAYMENT_STATUS, default "PENDING"
    amount: float
    refundAmount: float
    change: float
    applicationFee: float
    transfers: List[Transfer]
    refundedBy: str
    dojoRequestId: str
    dojoTerminalId: str
    tidyPay: TidyPay
    subTotal: float
    totalDiscountAmount: float
    serviceCharge: float
    tipAmount: float
    adyenTipAmount: float
    platformFee: float
    deliveryFee: float
    vendorFee: float
    stripeFee: float
    vatAt5: float
    vatAt12_5: float
    vatAt20: float
    transRefund: float
    redeemValue: float
    promotionDiscountAmount: float
    voucherDiscountAmount: float
    softwareFeePOS: FeeBreakdown
    softwareFeeRevenueShare: FeeBreakdown
    hardwareFee: FeeBreakdown
    softwareFeePOSTotal: float
    softwareFeeRevenueShareTotal: float
    hardwareFeeTotal: float
    adyen: AdyenTransaction
    error: str
    refundApplicationFee: float
    paymentIntent: Any
    cardData: CardData
    modeOfTransaction: str
    isSplitActive: bool
    taxes: TaxSetup
    paidByItem: bool
    paidItems: List[PaidItem]
    taxesNew: List[TaxEntry]
    inclusiveTaxTotal: float
    exclusiveTaxTotal: float
    tiers: List[TransactionTier]
    createdAt: datetime
    updatedAt: datetime


class ItemCategory(TypedDict, total=False):
    _id: ObjectId
    name: str
    vendorRef: ObjectId
    warehouseRef: ObjectId


class Promotion(TypedDict, total=False):
    promotionRef: ObjectId
    name: str
    promotionType: str
    savingType: str
    membershipId: str
    amount: float
    value: float
    quantity: float
    usageTimeFrequency: float
    fabricMemberId: str
    usageType: str
    maxUsage: float
    promoCode: str


class VoucherAppliedQuantityItem(TypedDict, total=False):
    itemRef: ObjectId
    voucherId: float
    limit: float
    name: str
    categoryRefId: ObjectId
    amount: float
    appliedAmount: float
    appliedQuantity: float
    sku: str
    variant: str
    itemMaxUsage: float


class Voucher(TypedDict, total=False):
    voucherRef: float
    voucherName: str
    voucherCode: str
    voucherType: str
    voucherAmount: float
    voucherRedeemAmount: float
    voucherToken: str
    voucherUserEmail: str
    voucherApplyToType: str
    voucherAppliedAmount: float
    voucherPercentageDiscount: float
    voucherAppliedQuantity: List[VoucherAppliedQuantityItem]


class ModifierVariant(TypedDict, total=False):
    variantName: str
    variantSellingPrice: float


class ModifierAsItem(TypedDict, total=False):
    _id: ObjectId
    itemId: str
    itemName: str
    itemSKU: str
    categoryRef: ItemCategory
    vendorRef: ObjectId
    parentItemRef: ObjectId
    warehouseRef: ObjectId
    supplierRef: List[ObjectId]
    itemImage: str
    sellingPrice: float
    costPrice: float
    vat: float
    hasVariants: bool
    ingredientsUsed: List[IngredientUsed]
    variants: List[ModifierVariant]


class Discount(TypedDict, total=False):
    discountRef: ObjectId
    quantity: float
    discountNote: str
    discountReason: str
    discountType: Optional[str]
    discountNumberType: Optional[str]
    discountAmount: float
    discountValue: float


class ModifierGroup(TypedDict, total=False):
    modifierGroupRef: Optional[ObjectId]
    displayName: str
    displayOrder: float
    selectionType: str  # enum: "Single", "Multiple", "Unlimited", ""
    maximumSelect: float
    feeType: str         # enum: "Free", "Paid", ""


class Modifier(TypedDict, total=False):
    itemRef: Optional[ObjectId]
    modifierGroup: ModifierGroup
    modifierRef: ObjectId
    name: str
    displayName: str
    costPrice: float
    price: float
    quantity: float
    subTotal: float
    item: ModifierAsItem
    totalDiscounts: float
    loyaltyDiscounts: float
    promotionDiscounts: float
    voucherDiscounts: float
    tipAmount: float
    serviceChargeAmount: float
    modifierFinalTotal: float
    modifierTotalTax: float
    discounts: List[Discount]
    vat: float
    flatDiscount: float
    taxSetup: TaxSetup
    taxesNew: List[TaxEntry]
    inclusiveTaxTotal: float
    exclusiveTaxTotal: float


class ItemPromotion(TypedDict, total=False):
    promotionRef: ObjectId
    name: str
    promotionType: str
    savingType: str
    amount: float
    value: float


class ItemRefund(TypedDict, total=False):
    refundRef: ObjectId
    quantity: float
    amount: float


class Variant(TypedDict, total=False):
    _id: str
    name: str
    sku: str
    price: float
    grossProfit: float
    markupMargin: float


class MenuRef(TypedDict, total=False):
    menuRef: Optional[ObjectId]
    displayName: str


class MenuGroup(TypedDict, total=False):
    menuGroupRef: Optional[ObjectId]
    groupName: str
    displayOrder: float


class Category(TypedDict, total=False):
    menuCategoryRef: Optional[ObjectId]
    categoryName: str


class AddedBy(TypedDict, total=False):
    _id: ObjectId
    firstName: str
    lastName: str
    employeeID: str


class ItemDetails(TypedDict, total=False):
    itemType: str               # enum: "manual", "item"
    parentItemRef: Optional[ObjectId]
    warehouseRef: Optional[ObjectId]
    displayOrder: float
    menu: MenuRef
    grossProfit: float
    markupMargin: float
    itemRef: ObjectId
    itemName: str
    vendorRef: Optional[ObjectId]
    menuGroup: MenuGroup
    category: Category
    price: float
    variant: Variant
    ingredientsUsed: List[IngredientUsed]
    costPrice: float
    modifiers: List[Modifier]
    isSent: bool
    sentAt: datetime
    quantity: float
    subTotal: float
    specialInstructions: str
    itemImage: str
    printerRef: Optional[ObjectId]
    assignedPrinters: List[ObjectId]
    kdsRef: Optional[ObjectId]
    kdsGroupRef: Optional[ObjectId]
    vat: float
    hasVariants: bool
    addedBy: AddedBy
    discounts: List[Discount]
    promotion: ItemPromotion
    totalDiscounts: float
    loyaltyDiscounts: float
    promotionDiscounts: float
    voucherDiscounts: float
    tipAmount: float
    serviceChargeAmount: float
    itemTotalTax: float
    itemFinalTotal: float
    assignedMenuItemRef: Optional[ObjectId]
    flatDiscount: float
    refunds: List[ItemRefund]
    isUpsell: bool
    taxSetup: TaxSetup
    afterTaxTotal: float
    itemBasedPromotionRef: ObjectId
    itemBasePromotionTotal: float
    taxesNew: List[TaxEntry]
    inclusiveTaxTotal: float
    exclusiveTaxTotal: float
    isItemTaxable: bool
    isDepositItem: bool


class ItemBasedPromotion(TypedDict, total=False):
    promotionRef: ObjectId
    name: str
    promotionType: str
    savingType: str
    amount: float
    value: float
    usageType: str
    maxUsage: float
    itemIds: List[ObjectId]


class UserRef(TypedDict, total=False):
    _id: ObjectId
    customerId: float
    firstName: str
    lastName: str
    userName: str
    email: str
    contactNo: str
    countryCode: str


class DojoRef(TypedDict, total=False):
    hostAddress: str
    apiKey: str
    installerId: str


class TidypayAccount(TypedDict, total=False):
    accountId: str
    tids: List[str]


class StripeFeeRate(TypedDict, total=False):
    variable: float
    fix: float


class StripeFeeInpersonEuro(TypedDict, total=False):
    debit: float
    debitFix: float
    credit: float
    creditFix: float
    amex: float
    amexFix: float


class StripeFee(TypedDict, total=False):
    onlineEuroFee: StripeFeeRate
    onlineNonEuroFee: StripeFeeRate
    inpersonNonEuroFee: StripeFeeRate
    inpersonEuroFee: StripeFeeInpersonEuro


class NoqFee(TypedDict, total=False):
    platform: float
    platformFix: float
    vendor: float
    vendorFix: float


class StripeConfig(TypedDict, total=False):
    stripeVendorId: Optional[str]
    stripeLocationId: Optional[str]
    stripeRegToken: Optional[str]


class AdyenVendor(TypedDict, total=False):
    balanceAccountId: Optional[str]
    storeId: Optional[str]
    feeType: str


class VendorDetails(TypedDict, total=False):
    _id: ObjectId
    name: str
    displayName: str
    contactEmail: str
    phone: str
    paymentGateway: str
    inPersonPaymentGateway: str
    mapImage: str
    outletImage: str
    receiptImage: str
    primaryColor: str
    primaryTextColor: str
    printerType: str
    isAutoAcceptActive: bool
    address: str
    address2: str
    countryCode: str
    timezone: str
    postalCode: str
    city: str
    landmark: Optional[str]
    country: Optional[str]
    vatNumber: Optional[str]
    storeType: str
    dojo: DojoRef
    stripe: StripeConfig
    stripeFee: StripeFee
    noqFee: NoqFee
    currency: str
    orderPrefix: str
    onlineOrderPrefix: str
    currencySymbol: str
    tidypay: List[TidypayAccount]
    adyen: AdyenVendor
    adyenInterchangeFee: dict
    adyenFee: FeeBreakdown
    onlineMerchantServiceAccountRef: Optional[ObjectId]
    inPersonMerchantServiceAccountRef: Optional[ObjectId]
    balanceAccountRef: Optional[ObjectId]
    adyenTerminalTipping: bool
    kdsActive: bool
    showAddressInCustomerReceipt: bool
    onlineOrderPrefixRequired: bool
    multiplePrintersEnabled: bool
    isMicroserviceActive: bool
    companyRegisterNumber: str


class Site(TypedDict, total=False):
    siteRef: Optional[ObjectId]
    splitArrangementRef: Optional[ObjectId]
    paymentFeeHolder: str
    displayName: str
    siteOwnership: str
    siteOwnerVendorRef: Optional[ObjectId]
    mapImage: str


class SiteZones(TypedDict, total=False):
    siteZoneRef: Optional[ObjectId]
    name: str


class Tip(TypedDict, total=False):
    value: float
    amount: float
    type: str


class LoyaltySchema(TypedDict, total=False):
    loyaltyRef: Optional[ObjectId]
    name: str
    earnPoint: float
    redeemValue: float
    pointsDelay: datetime


class EmployeeRef(TypedDict, total=False):
    _id: ObjectId
    firstName: str
    lastName: str
    employeeID: str


class Floor(TypedDict, total=False):
    floorName: str
    floorRef: Optional[ObjectId]
    layoutRef: Optional[ObjectId]


class OrderDiscount(TypedDict, total=False):
    itemArrayRef: List[ObjectId]
    itemRefs: List[ObjectId]
    menuCategoryRefs: List[ObjectId]
    menuGroupRefs: List[ObjectId]
    discountReason: str
    discountNote: str
    discountType: Optional[str]
    discountNumberType: Optional[str]
    discountAmount: float
    discountValue: float
    voucherId: float


class MergedTabData(TypedDict, total=False):
    tabRef: ObjectId
    tableNumber: str
    guestsNumber: float
    guestName: str
    totalAmount: float
    tabCreatedDate: datetime


class AutoPrint(TypedDict, total=False):
    printType: str
    numberOfPrintCopies: float


class DeliveryInfo(TypedDict, total=False):
    bagReturnOtp: str
    orderReturnOtp: str
    currentState: str
    name: str
    altPhone: str
    phone: str


class Reopen(TypedDict, total=False):
    isReopen: bool
    reopenTime: Optional[datetime]


# ── Main Order document ───────────────────────────────────────────────────────

class Order(TypedDict, total=False):
    _id: ObjectId
    orderNum: str
    orderId: float
    deliveryFee: float
    status: str               # enum: ORDER_STATUSES
    serviceType: str
    serviceTypeDisplayName: str
    cancelReason: str
    vendorRef: ObjectId
    items: List[ItemDetails]
    user: UserRef
    customerId: Optional[float]
    vendor: VendorDetails
    site: Site
    invitedBusinessRef: ObjectId
    siteZones: SiteZones
    preparationTime: float
    deliveryAddress: dict
    address: Optional[str]
    contactNumber: Optional[str]
    formattedContactNumber: Optional[str]
    specialInstructions: str
    currency: str
    tip: Tip
    totalAmount: float
    totalAmountAfterDiscount: float
    platformFee: float
    serviceCharge: float
    vendorTotal: float
    vendorFee: float
    cardData: CardData
    isArchived: bool
    userZoneIdentifier: Optional[str]
    note: str
    preOrder: bool
    deliveryDate: Optional[datetime]
    pickupDate: Optional[datetime]
    rejectReason: Optional[str]
    rejectDescription: Optional[str]
    preOrderSlotRef: Optional[ObjectId]
    applicationFee: float
    stripeFee: float
    subTotal: float
    collectionPoint: str
    vendorZoneName: Optional[str]
    source: str               # enum: SOURCE
    type: str                 # enum: ORDER_SOURCE + TAB_TYPE
    savedTabType: str
    vatAt5: float
    vatAt12_5: float
    vatAt20: float
    refundVatAt5: float
    refundVatAt12_5: float
    refundVatAt20: float
    vatPlatFormFee: float
    transactions: List[Transaction]
    tipAmount: float
    adyenTipAmount: float
    tabRef: Optional[ObjectId]
    tableNumber: str
    guestsNumber: float
    guestName: str
    tabOpenedTime: datetime
    openedBy: EmployeeRef
    closedBy: EmployeeRef
    floor: Floor
    totalDiscountAmount: float
    refundAmount: float
    discounts: List[OrderDiscount]
    newsLetter: bool
    promotion: Promotion
    promotionDiscountAmount: float
    voucher: Voucher
    voucherDiscountAmount: float
    loyalty: LoyaltySchema
    earnPoint: float
    redeemPoint: float
    redeemValue: float
    pointCreditedAt: Optional[datetime]
    preAuthNote: str
    prePaidOrder: bool
    counterDineType: str
    integrationType: str
    qrCodeUrl: Optional[str]
    extraFields: Optional[Any]
    adyenFee: float
    cartId: str
    checkoutType: str         # enum: ORDER_CHECKOUT_TYPE, default "STANDARD"
    appName: str
    appService: str
    isStockMinus: bool
    deviceId: str
    adyenDeviceId: str
    requiresUpdate: bool
    aggregatorsType: str
    aggregatorsOrderId: str
    orderType: str
    urbanPiperOrderRef: Optional[ObjectId]
    paymentLinkRef: Optional[ObjectId]
    urbanPiperOrderId: Optional[float]
    deliveryInfo: DeliveryInfo
    totalExternalDiscount: float
    urbanPiperDeliveryType: str
    urbanPiperExternalCharges: str
    cartRef: ObjectId
    isMultiOrder: bool
    orderReferenceNumber: str
    refundMigration: bool
    refundType: str           # enum: REFUND_TYPES
    mergedTabData: List[MergedTabData]
    autoPrint: AutoPrint
    domainOrderedFrom: str
    statusTimeStamps: dict
    statusChangeTimes: dict
    locationIdentifierLabel: str
    taxes: TaxSetup
    refundTaxes: TaxSetup
    taxesNew: List[TaxEntry]
    inclusiveTaxTotal: float
    exclusiveTaxTotal: float
    itemBasedPromotion: List[ItemBasedPromotion]
    reopen: Reopen
    businessId: Optional[ObjectId]
    countryCode: str
    transactionStarted: bool
    orderSequence: float
    offlineOrderId: str
    completedAt: Optional[datetime]
    isAdyenNotificationReceived: bool
    createdAt: datetime
    updatedAt: datetime
