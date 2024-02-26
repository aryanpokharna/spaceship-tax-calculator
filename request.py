def request_json(type):
    if type == "login_pre_mfa":
        return request["login"]["login_pre_MFA"]
    if type == "login_post_mfa":
        return request["login"]["login_post_MFA"]
    if type == "transaction":
        return request["data"]["transaction"]
    if type == "logout":
        return request["logout"]

def header_json(type):
    if type == "header":
        return header["data"]["transaction"]
    
def update_request(credentials):

    # update login pre MFA request
    request["login"]["login_pre_MFA"]["variables"]["input"]["email"] = credentials.email
    request["login"]["login_pre_MFA"]["variables"]["input"]["password"] = credentials.password

    # update login post MFA request
    request["login"]["login_post_MFA"]["variables"]["input"]["email"] = credentials.email
    request["login"]["login_post_MFA"]["variables"]["input"]["password"] = credentials.password
    request["login"]["login_post_MFA"]["variables"]["input"]["mfaAnswer"]["id"] = credentials.user_id
    request["login"]["login_post_MFA"]["variables"]["input"]["mfaAnswer"]["token"] = credentials.mfa_code

    # update logout request
    request["logout"]["variables"]["input"]["id"] = credentials.user_id

def update_header(credentials):
    header["data"]["transaction"]["Authorization"] = credentials.bearer

request = { 
    "login" : {
        "login_pre_MFA" : {
            "operationName": "Login",
            "query": """
                mutation Login($input: LoginInput!) {
                    login(input: $input) {
                        auth {
                            authToken
                            id
                            refreshToken
                            scopes
                        }
                        intercomHashes {
                            android
                            id
                            ios
                            web
                        }
                        mfaChallenge {
                            id
                            type
                        }
                    }
                }
            """,
            "variables": {
                "input": {
                    "email": None,
                    "password": None
                }
            }
        },
        "login_post_MFA" : {
            "operationName": "Login",
            "query": """
                mutation Login($input: LoginInput!) {
                    login(input: $input) {
                        auth {
                            authToken
                            id
                            refreshToken
                            scopes
                        }
                        intercomHashes {
                            android
                            id
                            ios
                            web
                        }
                        mfaChallenge {
                            id
                            type
                        }
                    }
                }
            """,
            "variables": {
                "input": {
                    "email": None,
                    "mfaAnswer": {
                        "id": None,
                        "token": None,
                    },
                    "password": None
                }
            }
        }
    },
    "data" : {
        "transaction" : {
            "operationName": "WebAppVoyagerDashboard",
            "query": "query WebAppVoyagerDashboard($tmdManuallyApprovedIndexCardDismissibleId: String!, $tmdManuallyApprovedUniverseCardDismissibleId: String!, $tmdManuallyApprovedEarthCardDismissibleId: String!) {\n  contact {\n    id\n    firstName\n    preferredName\n    phoneNumberVerified\n    account {\n      id\n      saverProductInstances {\n        id\n        primary\n        portfolio\n        portfolioPerformance {\n          ...voyagerPortfolioPerformanceFields\n          __typename\n        }\n        boostRecipes {\n          id\n          name\n          iconName\n          groups {\n            id\n            status\n            audAmount\n            cancellableUntil\n            __typename\n          }\n          __typename\n        }\n        upcomingSchedule {\n          id\n          frequency\n          audAmount\n          nextDue\n          __typename\n        }\n        investments {\n          id\n          summary {\n            id\n            ...investmentSummaryScalars\n            __typename\n          }\n          transactions {\n            id\n            audAmount\n            requestedAt\n            status\n            unitExchange {\n              id\n              ...unitExchangeScalars\n              unitPrice {\n                id\n                ...unitPriceScalars\n                __typename\n              }\n              __typename\n            }\n            ... on Referral {\n              isReferrer\n              referralShortName\n              referrerShortName\n              __typename\n            }\n            ... on Redemption {\n              redemptionBankAccount: bankAccount {\n                id\n                ...bankAccountScalars\n                __typename\n              }\n              __typename\n            }\n            ... on Application {\n              estimatedExecutionDate\n              cancelDeadline\n              schedule {\n                id\n                ...scheduleScalars\n                __typename\n              }\n              applicationBankAccount: bankAccount {\n                id\n                ...bankAccountScalars\n                __typename\n              }\n              __typename\n            }\n            ... on Boost {\n              estimatedExecutionDate\n              itemGroup {\n                id\n                recipe {\n                  id\n                  name\n                  __typename\n                }\n                __typename\n              }\n              boostBankAccount: bankAccount {\n                id\n                ...bankAccountScalars\n                __typename\n              }\n              __typename\n            }\n            ... on AccountFee {\n              type\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        dailyBalances {\n          date\n          audAmount\n          __typename\n        }\n        __typename\n      }\n      saverReferralShareDetails {\n        id\n        status\n        __typename\n      }\n      ...voyagerReferralsCardFields\n      __typename\n    }\n    ...webAppVoyagerBoostsCard\n    __typename\n  }\n  articles {\n    id\n    ...webAppArticleCardFragment\n    __typename\n  }\n  ...ShowTmdManuallyApprovedCard_QueryFragment\n}\n\nfragment investmentSummaryScalars on InvestmentSummary {\n  id\n  unitBalance\n  audBalance\n  audInvested\n  audWithdrawn\n  audReferralTotal\n  audPromotionTotal\n  audMarketReturn\n  audAccountFeesPaid\n  __typename\n}\n\nfragment bankAccountScalars on BankAccount {\n  id\n  accountNumber\n  bsb\n  friendlyName\n  accountName\n  createdAt\n  lastUpdatedAt\n  __typename\n}\n\nfragment unitExchangeScalars on UnitExchange {\n  id\n  units\n  createdAt\n  __typename\n}\n\nfragment unitPriceScalars on UnitPrice {\n  id\n  price\n  effectiveDate\n  __typename\n}\n\nfragment scheduleScalars on Schedule {\n  id\n  frequency\n  audAmount\n  nextDue\n  __typename\n}\n\nfragment webAppArticleCardFragment on Article {\n  id\n  heading\n  subheading\n  articleUrl\n  imageUrl\n  publication\n  publicationUrl\n  instrument {\n    id\n    name\n    audLatestPrice\n    audMarketCapitalisation\n    ytdPercentageChange\n    portfolios\n    __typename\n  }\n  __typename\n}\n\nfragment voyagerReferralsCardFields on Account {\n  id\n  saverReferralShareDetails {\n    id\n    status\n    code\n    campaign {\n      id\n      title\n      audReceiverRewardAmount\n      audSharerRewardAmount\n      audReceiverMinimumInvestmentAmount\n      audSharerMinimumInvestmentAmount\n      endDate\n      __typename\n    }\n    rewardDestinationProductInstance {\n      id\n      __typename\n    }\n    __typename\n  }\n  saverReferralReceiveDetails {\n    id\n    status\n    referrerShortName\n    campaign {\n      id\n      audReceiverRewardAmount\n      audReceiverMinimumInvestmentAmount\n      __typename\n    }\n    rewardDestinationProductInstance {\n      id\n      upcomingSchedule {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment webAppVoyagerBoostsCard on Contact {\n  id\n  account {\n    id\n    saverBoostRecipes {\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment saverTmdDetailsFields on SaverTMDDetails {\n  createdAt\n  result\n  submissionAvailable\n  resubmissionConfirmationRequired\n  reviewedAt\n  __typename\n}\n\nfragment ShowTmdManuallyApprovedCard_QueryFragment on Query {\n  indexTmdManuallyApprovedCardDismissible: dismissible(\n    id: $tmdManuallyApprovedIndexCardDismissibleId\n  ) {\n    id\n    hidden\n    __typename\n  }\n  universeTmdManuallyApprovedCardDismissible: dismissible(\n    id: $tmdManuallyApprovedUniverseCardDismissibleId\n  ) {\n    id\n    hidden\n    __typename\n  }\n  earthTmdManuallyApprovedCardDismissible: dismissible(\n    id: $tmdManuallyApprovedEarthCardDismissibleId\n  ) {\n    id\n    hidden\n    __typename\n  }\n  contact {\n    id\n    account {\n      id\n      saverProductInstances {\n        id\n        createdAt\n        primary\n        portfolio\n        upcomingSchedule {\n          id\n          __typename\n        }\n        latestInvestments: investments {\n          id\n          transactions(limit: 1) {\n            id\n            ... on Application {\n              schedule {\n                id\n                ...scheduleScalars\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      indexSaverTMDDetails: saverTMDDetails(portfolio: INDEX) {\n        ...saverTmdDetailsFields\n        __typename\n      }\n      universeSaverTMDDetails: saverTMDDetails(portfolio: UNIVERSE) {\n        ...saverTmdDetailsFields\n        __typename\n      }\n      earthSaverTMDDetails: saverTMDDetails(portfolio: EARTH) {\n        ...saverTmdDetailsFields\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment voyagerPortfolioPerformanceFields on SaverPortfolioPerformance {\n  oneDayPerformancePercentage\n  oneWeekPerformancePercentage\n  oneMonthPerformancePercentage\n  oneYearPerformancePercentage\n  __typename\n}\n",
            "variables": {
                "tmdManuallyApprovedIndexCardDismissibleId": "tmd_manually_approved_index_card",
                "tmdManuallyApprovedUniverseCardDismissibleId": "tmd_manually_approved_universe_card",
                "tmdManuallyApprovedEarthCardDismissibleId": "tmd_manually_approved_earth_card"
            }
        }
    },
    "logout" : {
        "operationName": "RevokeSession",
        "query": "mutation RevokeSession($input: RevokeSessionInput!) {\n  revokeSession(input: $input) {\n    id\n  }\n}\n",
        "variables": {
            "input": {
                "id": None
            }
        }
    }
}

header = {
    "data" : {
        "transaction" : {
            "Authorization": None,
            "Content-Type": "application/json",
        }
    }
}