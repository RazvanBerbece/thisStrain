//
//  requester.swift
//  thisStrain
//
//  Created by Razvan-Antonio Berbece on 06/06/2020.
//  Copyright © 2020 Razvan-Antonio Berbece. All rights reserved.
//

import Foundation
import Alamofire
import SwiftyJSON

public class Client {
    
    private let url : String = "http://192.168.0.39:5000"
    
    public func testAPIAvailability() {
        AF.request(self.url + "/", method: .get).responseJSON {
            response in
            print(response)
        }
    }
    
    public func sendPostWithData(base64string: String, completion: @escaping ([String]) -> Void) {
        AF.upload(multipartFormData: {
            (multipartFormData) in
            multipartFormData.append(Data(base64string.utf8), withName: "data")
        }, to: self.url + "/predictOnImage", method: .post).responseJSON {
            (response) in
            if let status = response.response?.statusCode {
                switch (status) {
                case 200:
                    if let data = response.data {
                        if let json = try? JSON(data: data) {
                            completion([String(describing: json["output"][0]), String(describing: json["output"][1])])
                        }
                    }
                    break
                default:
                    print("ERROR WITH STATUS CODE : \(status)")
                    completion(["", ""])
                }
            }
        }
    }
    
}
