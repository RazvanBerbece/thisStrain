//
//  encoder.swift
//  thisStrain
//
//  Created by Razvan-Antonio Berbece on 06/06/2020.
//  Copyright © 2020 Razvan-Antonio Berbece. All rights reserved.
//

import Foundation
import UIKit

public class Base64Encoder {
    
    public func imageToBase64(image: UIImage) -> String {
        let cimg = CIImage(image: image)
        if cimg != nil {
            let imageData = image.highestQualityJPEGNSData
            return imageData.base64EncodedString(options: NSData.Base64EncodingOptions.lineLength64Characters)
        }
        return ""
    }
    
}

extension UIImage {
    var highestQualityJPEGNSData:NSData { return self.jpegData(compressionQuality: 1.0)! as NSData }
    var highQualityJPEGNSData:NSData    { return self.jpegData(compressionQuality: 0.75)! as NSData}
    var mediumQualityJPEGNSData:NSData  { return self.jpegData(compressionQuality: 0.5)! as NSData }
    var lowQualityJPEGNSData:NSData     { return self.jpegData(compressionQuality: 0.25)! as NSData}
    var lowestQualityJPEGNSData:NSData  { return self.jpegData(compressionQuality: 0.0)! as NSData }
}
